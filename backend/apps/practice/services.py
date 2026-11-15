from __future__ import annotations

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ValidationError

from apps.catalog.models import Topic
from apps.core.models import AuditEvent
from apps.practice.models import AttemptAnswer, PracticeSession, SessionItem
from apps.questions.models import Question


class Conflict(APIException):
    status_code = 409
    default_detail = "The item is not in a state that allows that action."
    default_code = "conflict"


def _require_auth(actor):
    if not actor or not actor.is_authenticated:
        raise PermissionDenied("Authentication required.")


def _audit(actor, action: str, target, metadata: dict | None = None) -> None:
    AuditEvent.objects.create(
        actor=actor,
        action=action,
        object_type=f"{target.__class__.__module__}.{target.__class__.__name__}",
        object_id=target.pk,
        metadata=metadata or {},
    )


def _get_topic_and_exam_version(topic_identifier):
    # Expect a UUID of a Topic; later may support subject/exam_version params.
    try:
        topic = Topic.objects.get(pk=topic_identifier)
    except Topic.DoesNotExist:
        raise NotFound("Topic not found.") from None
    exam_version = topic.subject.exam_version
    if exam_version is None:
        raise ValidationError({"topic": ["The topic does not have an exam version defined."]})
    return exam_version, topic


@transaction.atomic
def start_session(actor, *, mode, topic_identifier, size=20):
    _require_auth(actor)
    exam_version, topic = _get_topic_and_exam_version(topic_identifier)
    # Ensure there are published items for the topic.
    if not Question.objects.filter(topic=topic, status=Question.Status.PUBLISHED).exists():
        raise ValidationError({"topic": ["No published items for this topic."]})
    published_count = Question.objects.filter(topic=topic, status=Question.Status.PUBLISHED).count()
    if size > published_count:
        size = published_count

    session = PracticeSession.objects.create(
        user=actor,
        exam_version=exam_version,
        mode=mode,
        status=PracticeSession.Status.IN_PROGRESS,
        time_limit_seconds=60 if mode == PracticeSession.Mode.TIMED else None,
        started_at=timezone.now(),
    )
    if session.mode == PracticeSession.Mode.TIMED:
        session.expires_at = session.started_at + timezone.timedelta(
            seconds=session.time_limit_seconds
        )
        session.save(update_fields=["expires_at"])

    questions = list(
        Question.objects.filter(
            topic=topic,
            status=Question.Status.PUBLISHED,
        ).order_by("id")[:size]
    )
    session_items = []
    for i, question in enumerate(questions):
        session_items.append(
            SessionItem(
                session=session,
                question=question,
                display_order=i,
                snapshot_stem=question.stem,
                snapshot_options=[
                    {"id": str(c.id), "text": c.text, "is_correct": c.is_correct}
                    for c in question.choices.all()
                ],
                snapshot_explanation=question.explanation,
                snapshot_provenance=question.provenance,
                snapshot_difficulty=question.difficulty,
            )
        )
    SessionItem.objects.bulk_create(session_items)
    _audit(actor, AuditEvent.Action.PRACTICE_SESSION_STARTED, session, {"topic": str(topic.pk)})
    return session


def _is_expired(session) -> bool:
    return bool(
        session.mode == PracticeSession.Mode.TIMED
        and session.expires_at
        and timezone.now() >= session.expires_at
    )


def _finalize_session(session) -> None:
    """Score saved answers once and mark the session submitted."""
    total = 0
    correct = 0
    answers_to_update = []
    for item in session.items.select_related("question"):
        total += 1
        answer = item.answers.first()
        if not answer:
            continue
        is_correct = False
        if answer.selected_choice_id:
            snapshot_options = {opt["id"]: opt["is_correct"] for opt in item.snapshot_options}
            is_correct = snapshot_options.get(str(answer.selected_choice_id), False)
        if is_correct:
            correct += 1
        answer.is_correct = is_correct
        answers_to_update.append(answer)
    if answers_to_update:
        AttemptAnswer.objects.bulk_update(answers_to_update, ["is_correct"])
    session.status = PracticeSession.Status.SUBMITTED
    session.submitted_at = timezone.now()
    session.score_correct = correct
    session.score_total = total
    session.save(update_fields=["status", "submitted_at", "score_correct", "score_total"])


def _submit(session, actor, *, expired: bool = False):
    _finalize_session(session)
    action = (
        AuditEvent.Action.PRACTICE_SESSION_EXPIRED
        if expired
        else AuditEvent.Action.PRACTICE_SESSION_SUBMITTED
    )
    _audit(actor, action, session)
    return session


@transaction.atomic
def get_session(actor, session_id):
    _require_auth(actor)
    try:
        session = PracticeSession.objects.get(pk=session_id, user=actor)
    except PracticeSession.DoesNotExist:
        raise NotFound("Practice session not found.") from None
    if session.status not in (PracticeSession.Status.IN_PROGRESS, PracticeSession.Status.SUBMITTED):
        raise PermissionDenied("Session not accessible.")
    if session.status == PracticeSession.Status.IN_PROGRESS and _is_expired(session):
        _submit(session, actor, expired=True)
    return session


@transaction.atomic
def save_answer(actor, session_id, position, selected_choice_id):
    _require_auth(actor)
    try:
        session_item = SessionItem.objects.select_related("session", "question").get(
            session_id=session_id,
            display_order=position,
        )
    except SessionItem.DoesNotExist:
        raise NotFound("Session item not found.") from None
    if session_item.session.user_id != actor.pk:
        raise PermissionDenied("You do not own this session.")
    if session_item.session.status != PracticeSession.Status.IN_PROGRESS:
        raise Conflict("Session is not in progress.")
    if _is_expired(session_item.session):
        raise Conflict("Session expired.")
    if selected_choice_id:
        try:
            session_item.question.choices.get(pk=selected_choice_id)
        except Question.DoesNotExist:
            raise ValidationError({"selected_choice_id": ["Invalid choice."]}) from None
    answer, _ = AttemptAnswer.objects.get_or_create(
        session_item=session_item,
        defaults={"selected_choice_id": selected_choice_id, "answered_at": timezone.now()},
    )
    if not answer.selected_choice_id and selected_choice_id:
        answer.selected_choice_id = selected_choice_id
        answer.answered_at = timezone.now()
        answer.save()
    return answer


@transaction.atomic
def submit_session(actor, session_id):
    _require_auth(actor)
    try:
        session = PracticeSession.objects.select_related("user").get(pk=session_id)
    except PracticeSession.DoesNotExist:
        raise NotFound("Practice session not found.") from None
    if session.user_id != actor.pk:
        raise PermissionDenied("You do not own this session.")
    if session.status == PracticeSession.Status.SUBMITTED:
        # Idempotent submit: return the existing result.
        return session
    if session.status != PracticeSession.Status.IN_PROGRESS:
        raise Conflict("Session is not in progress.")
    return _submit(session, actor, expired=_is_expired(session))


@transaction.atomic
def get_session_results(actor, session_id):
    _require_auth(actor)
    try:
        session = (
            PracticeSession.objects.select_related("user", "exam_version")
            .prefetch_related("items__question__choices")
            .get(pk=session_id, user=actor)
        )
    except PracticeSession.DoesNotExist:
        raise NotFound("Practice session not found.") from None
    if session.status == PracticeSession.Status.IN_PROGRESS and _is_expired(session):
        _submit(session, actor, expired=True)
    if session.status != PracticeSession.Status.SUBMITTED:
        raise PermissionDenied("Results are only available after submission.")
    results = {
        "session_id": str(session.id),
        "score_correct": session.score_correct,
        "score_total": session.score_total,
        "items": [],
    }
    for item in session.items.all():
        answer = item.answers.first()
        snapshot_options = [
            {"id": opt["id"], "text": opt["text"], "is_correct": opt["is_correct"]}
            for opt in item.snapshot_options
        ]
        results["items"].append(
            {
                "position": item.display_order,
                "question": {
                    "id": str(item.question_id),
                    "stem": item.snapshot_stem,
                    "options": snapshot_options,
                    "explanation": item.snapshot_explanation,
                    "provenance": item.snapshot_provenance,
                    "difficulty": item.snapshot_difficulty,
                },
                "selected_option_id": str(answer.selected_choice_id)
                if answer and answer.selected_choice_id
                else None,
                "is_correct": answer.is_correct if answer else None,
                "explanation": item.snapshot_explanation,
                "provenance": item.snapshot_provenance,
            }
        )
    return results


def get_session_history(actor, page=1, page_size=20):
    _require_auth(actor)
    qs = PracticeSession.objects.filter(user=actor).order_by("-started_at")
    return qs
