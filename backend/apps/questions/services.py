from __future__ import annotations

import hashlib

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ValidationError

from apps.catalog.models import Topic
from apps.core.models import AuditEvent
from apps.questions.models import Choice, ContentFlag, Question


class Conflict(APIException):
    status_code = 409
    default_detail = "The item is not in a state that allows that action."
    default_code = "conflict"


def normalize_stem(stem: str) -> str:
    return " ".join(stem.split()).lower()


def stem_hash(stem: str) -> str:
    return hashlib.sha256(normalize_stem(stem).encode()).hexdigest()


def _require_staff(actor) -> None:
    if not actor.is_staff:
        raise PermissionDenied("You do not have permission to do that.")


def _audit(actor, action: str, question: Question, metadata: dict | None = None) -> None:
    AuditEvent.objects.create(
        actor=actor,
        action=action,
        object_type="questions.Question",
        object_id=question.pk,
        metadata=metadata or {},
    )


def _flag_audit(actor, action: str, flag: ContentFlag, metadata: dict | None = None) -> None:
    AuditEvent.objects.create(
        actor=actor,
        action=action,
        object_type="questions.ContentFlag",
        object_id=flag.pk,
        metadata=metadata or {},
    )


@transaction.atomic
def create_question(
    actor,
    *,
    topic_id,
    stem: str,
    options: list[dict],
    correct_answer_index: int,
    explanation: str = "",
    provenance: str = "",
    difficulty: int = 3,
) -> Question:
    """Create a draft item. Publishing is a separate, reviewed transition."""
    _require_staff(actor)
    topic = Topic.objects.filter(pk=topic_id).first()
    if topic is None:
        raise NotFound("Topic not found.")
    if not 2 <= len(options) <= 6:
        raise ValidationError({"options": ["Provide between 2 and 6 options."]})
    if not 0 <= correct_answer_index < len(options):
        raise ValidationError({"correct_answer_index": ["Select one of the provided options."]})

    question = Question.objects.create(
        topic=topic,
        stem=stem,
        stem_hash=stem_hash(stem),
        explanation=explanation,
        provenance=provenance,
        difficulty=difficulty,
        author=actor,
    )
    Choice.objects.bulk_create(
        [
            Choice(
                question=question,
                text=option["text"],
                rationale=option["rationale"],
                is_correct=index == correct_answer_index,
                display_order=index,
            )
            for index, option in enumerate(options)
        ]
    )
    _audit(actor, AuditEvent.Action.QUESTION_CREATED, question, {"topic_id": str(topic.pk)})
    return question


def submit_for_review(actor, question: Question) -> Question:
    _require_staff(actor)
    if question.status != Question.Status.DRAFT:
        raise Conflict("Only draft items can be submitted for review.")
    question.status = Question.Status.IN_REVIEW
    question.save(update_fields=["status", "updated_at"])
    _audit(actor, AuditEvent.Action.QUESTION_SUBMITTED_FOR_REVIEW, question)
    return question


@transaction.atomic
def review_question(actor, question: Question, *, approve: bool, reason: str = "") -> Question:
    """Approve (publish) or reject an item. Self-review is never allowed."""
    _require_staff(actor)
    if question.author_id == actor.pk:
        raise PermissionDenied("You cannot review your own item.")
    if question.status != Question.Status.IN_REVIEW:
        raise Conflict("Only items in review can be reviewed.")

    if approve:
        fields = {}
        if not question.explanation.strip():
            fields["explanation"] = ["Required before publishing."]
        if not question.provenance.strip():
            fields["provenance"] = ["Required before publishing."]
        if fields:
            raise ValidationError(fields)
        question.status = Question.Status.PUBLISHED
        action = AuditEvent.Action.QUESTION_PUBLISHED
    else:
        question.status = Question.Status.DRAFT
        action = AuditEvent.Action.QUESTION_REVIEW_REJECTED

    question.reviewer = actor
    question.reviewed_at = timezone.now()
    question.save(update_fields=["status", "reviewer", "reviewed_at", "updated_at"])
    _audit(actor, action, question, {"reason": reason})
    return question


def retire_question(actor, question: Question, reason: str = "") -> Question:
    """Remove a published item from new sets; attempts keep their snapshot."""
    _require_staff(actor)
    if question.status != Question.Status.PUBLISHED:
        raise Conflict("Only published items can be retired.")
    question.status = Question.Status.RETIRED
    question.save(update_fields=["status", "updated_at"])
    _audit(actor, AuditEvent.Action.QUESTION_RETIRED, question, {"reason": reason})
    return question


def create_flag(actor, question: Question, *, reason: str, note: str = "") -> ContentFlag:
    """Learners may flag published or retired items they have seen."""
    if question.status not in (Question.Status.PUBLISHED, Question.Status.RETIRED):
        raise NotFound("Item not found.")
    if ContentFlag.objects.filter(
        question=question, reporter=actor, status=ContentFlag.Status.OPEN
    ).exists():
        raise Conflict("You already flagged this item. Staff are reviewing it.")

    flag = ContentFlag.objects.create(
        question=question,
        reporter=actor,
        reason=reason,
        note=note,
    )
    _flag_audit(actor, AuditEvent.Action.FLAG_CREATED, flag)
    return flag


def resolve_flag(actor, flag: ContentFlag, *, dismiss: bool = False, note: str = "") -> ContentFlag:
    _require_staff(actor)
    if flag.status != ContentFlag.Status.OPEN:
        raise Conflict("This flag is already closed.")
    flag.status = ContentFlag.Status.DISMISSED if dismiss else ContentFlag.Status.RESOLVED
    flag.resolved_by = actor
    flag.resolved_at = timezone.now()
    flag.resolution_note = note
    flag.save(
        update_fields=["status", "resolved_by", "resolved_at", "resolution_note", "updated_at"]
    )
    action = AuditEvent.Action.FLAG_DISMISSED if dismiss else AuditEvent.Action.FLAG_RESOLVED
    _flag_audit(actor, action, flag)
    return flag
