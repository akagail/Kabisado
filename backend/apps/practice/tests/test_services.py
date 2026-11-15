from __future__ import annotations

import pytest
from django.core.management import call_command
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.practice import services
from apps.practice.models import PracticeSession
from apps.questions.models import Question
from apps.questions.services import create_question, review_question, submit_for_review

pytestmark = pytest.mark.django_db


def _topic():
    call_command("seed_cse_catalogue", force=True)
    return Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )


def _staff(email="curator@example.com"):
    return User.objects.create_user(email=email, password="CorrectHorse123!", is_staff=True)


def _create_published_question(topic, author):
    question = create_question(
        author,
        topic_id=topic.pk,
        stem="What is 2 + 2?",
        options=[
            {"text": "3", "rationale": "Incorrect."},
            {"text": "4", "rationale": "Correct."},
        ],
        correct_answer_index=1,
        explanation="Two plus two is four.",
        provenance="Original item.",
    )
    submit_for_review(author, question)
    reviewer = User.objects.create_user(
        email="reviewer@example.com", password="CorrectHorse123!", is_staff=True
    )
    review_question(reviewer, question, approve=True)
    return question


def _published_question_count(topic):
    return Question.objects.filter(topic=topic, status=Question.Status.PUBLISHED).count()


def test_start_untimed_session():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    count = _published_question_count(topic)
    session = services.start_session(
        actor, mode="untimed", topic_identifier=str(topic.pk), size=count
    )

    assert session.user == actor
    assert session.mode == "untimed"
    assert session.status == "in_progress"
    assert session.items.count() == count
    # All session items should have snapshot data
    for item in session.items.all():
        assert item.snapshot_stem
        assert item.snapshot_options
        assert item.snapshot_explanation
        assert item.snapshot_provenance
        assert item.snapshot_difficulty


def test_start_timed_session():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    count = _published_question_count(topic)
    session = services.start_session(
        actor, mode="timed", topic_identifier=str(topic.pk), size=count
    )

    assert session.mode == "timed"
    assert session.time_limit_seconds == 60
    assert session.expires_at is not None


def test_start_session_without_permission():
    from django.contrib.auth.models import AnonymousUser

    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    with pytest.raises(PermissionDenied):
        services.start_session(AnonymousUser(), mode="untimed", topic_identifier=str(topic.pk))


def test_start_session_no_published_items():
    topic = _topic()
    actor = _staff()
    with pytest.raises(ValidationError):
        services.start_session(actor, mode="untimed", topic_identifier=str(topic.pk))


def test_expired_timed_session_auto_submits_on_read():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    session = services.start_session(actor, mode="timed", topic_identifier=str(topic.pk), size=1)
    PracticeSession.objects.filter(pk=session.pk).update(
        expires_at=timezone.now() - timezone.timedelta(seconds=1)
    )

    result = services.get_session(actor, session.id)
    assert result.status == "submitted"
    assert result.score_correct == 0
    assert result.score_total == 1


def test_submit_session_before_answers():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    count = _published_question_count(topic)
    session = services.start_session(
        actor, mode="untimed", topic_identifier=str(topic.pk), size=count
    )
    # No answers saved: submit should still succeed, scoring zero correct.
    result = services.submit_session(actor, session.id)
    assert result.status == "submitted"
    assert result.score_correct == 0
    assert result.score_total == count


def test_save_answer():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    count = _published_question_count(topic)
    session = services.start_session(
        actor, mode="untimed", topic_identifier=str(topic.pk), size=count
    )
    # Get the first question's first choice (we need to fetch a choice id)
    question = session.items.first().question
    choice_id = question.choices.first().id

    answer = services.save_answer(actor, session.id, 0, choice_id)
    assert answer.selected_choice_id == choice_id
    assert answer.is_correct is None  # not computed yet


def test_submit_session_after_answers():
    topic = _topic()
    actor = _staff()
    _create_published_question(topic, actor)
    count = _published_question_count(topic)
    session = services.start_session(
        actor, mode="untimed", topic_identifier=str(topic.pk), size=count
    )
    # There should be exactly one item
    assert session.items.count() == 1
    item = session.items.first()
    question = item.question
    # Select the correct choice so the score is 1.
    choice = question.choices.get(is_correct=True)
    choice_id = choice.id
    answer = services.save_answer(actor, session.id, 0, choice_id)

    result = services.submit_session(actor, session.id)
    assert result.status == "submitted"
    assert result.score_correct == 1
    assert result.score_total == 1  # one answered
    answer = session.items.first().answers.first()
    assert answer.is_correct is True
