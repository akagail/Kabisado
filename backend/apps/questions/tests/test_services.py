from __future__ import annotations

import pytest
from django.core.management import call_command
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.core.models import AuditEvent
from apps.questions import selectors, services
from apps.questions.models import ContentFlag, Question
from apps.questions.services import Conflict, create_question

pytestmark = pytest.mark.django_db


def _topic() -> Topic:
    call_command("seed_cse_catalogue", force=True)
    return Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )


def _user(email: str, *, staff: bool = False) -> User:
    return User.objects.create_user(email=email, password="CorrectHorse123!", is_staff=staff)


def _create(author: User, topic: Topic, *, explanation: str = "Because.") -> Question:
    return create_question(
        author,
        topic_id=topic.pk,
        stem="What is 1 + 1?",
        options=[
            {"text": "1", "rationale": "Incorrect."},
            {"text": "2", "rationale": "Correct."},
        ],
        correct_answer_index=1,
        explanation=explanation,
        provenance="Original item.",
    )


def _published(author: User, reviewer: User, topic: Topic) -> Question:
    question = _create(author, topic)
    services.submit_for_review(author, question)
    services.review_question(reviewer, question, approve=True)
    return question


def test_create_question_records_options_and_audit():
    topic = _topic()
    author = _user("author@example.com", staff=True)

    question = _create(author, topic)

    assert question.status == Question.Status.DRAFT
    assert question.author == author
    assert question.choices.count() == 2
    assert question.choices.filter(is_correct=True).count() == 1
    assert AuditEvent.objects.filter(
        action=AuditEvent.Action.QUESTION_CREATED, object_id=question.pk
    ).exists()


def test_publish_requires_explanation_and_provenance():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    question = _create(author, topic, explanation="")
    services.submit_for_review(author, question)

    with pytest.raises(ValidationError):
        services.review_question(reviewer, question, approve=True)

    question.refresh_from_db()
    assert question.status == Question.Status.IN_REVIEW


def test_self_review_is_forbidden():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    question = _create(author, topic)
    services.submit_for_review(author, question)

    with pytest.raises(PermissionDenied):
        services.review_question(author, question, approve=True)


def test_reject_returns_item_to_draft_and_audits():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    question = _create(author, topic)
    services.submit_for_review(author, question)

    services.review_question(reviewer, question, approve=False, reason="Needs a source.")

    question.refresh_from_db()
    assert question.status == Question.Status.DRAFT
    assert question.reviewer == reviewer
    assert AuditEvent.objects.filter(
        action=AuditEvent.Action.QUESTION_REVIEW_REJECTED, object_id=question.pk
    ).exists()


def test_retire_removes_item_from_new_sets_only_after_publish():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    question = _create(author, topic)

    with pytest.raises(Conflict):
        services.retire_question(reviewer, question)

    services.submit_for_review(author, question)
    services.review_question(reviewer, question, approve=True)
    services.retire_question(reviewer, question, reason="Wrong key.")

    assert selectors.published_questions_for_topic(topic.pk).count() == 0
    assert AuditEvent.objects.filter(
        action=AuditEvent.Action.QUESTION_RETIRED, object_id=question.pk
    ).exists()


def test_learner_cannot_manage_questions():
    topic = _topic()
    learner = _user("learner@example.com")

    with pytest.raises(PermissionDenied):
        _create(learner, topic)


def test_flag_lifecycle_merges_duplicates_and_audits():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")
    question = _published(author, reviewer, topic)

    flag = services.create_flag(learner, question, reason="typo", note="Missing period.")

    with pytest.raises(Conflict):
        services.create_flag(learner, question, reason="unclear")

    services.resolve_flag(reviewer, flag, note="Fixed.")
    flag.refresh_from_db()
    assert flag.status == ContentFlag.Status.RESOLVED
    assert flag.resolved_by == reviewer

    # One open flag per reporter; a resolved flag allows a fresh report.
    reopened = services.create_flag(learner, question, reason="unclear")
    assert reopened.pk != flag.pk

    actions = set(AuditEvent.objects.values_list("action", flat=True))
    assert {
        AuditEvent.Action.FLAG_CREATED,
        AuditEvent.Action.FLAG_RESOLVED,
    } <= actions


def test_learner_cannot_resolve_flags():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")
    question = _published(author, reviewer, topic)
    flag = services.create_flag(learner, question, reason="typo")

    with pytest.raises(PermissionDenied):
        services.resolve_flag(learner, flag)


def test_flagging_a_draft_is_not_found():
    topic = _topic()
    author = _user("author@example.com", staff=True)
    learner = _user("learner@example.com")
    question = _create(author, topic)

    with pytest.raises(NotFound):
        services.create_flag(learner, question, reason="typo")
