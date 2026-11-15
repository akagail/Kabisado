from __future__ import annotations

import pytest
from django.core.management import call_command
from django.db import IntegrityError

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.questions.models import Choice, ContentFlag, Question
from apps.questions.services import create_question, stem_hash

pytestmark = pytest.mark.django_db


def _topic() -> Topic:
    call_command("seed_cse_catalogue", force=True)
    return Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )


def _staff(email: str = "curator@example.com") -> User:
    return User.objects.create_user(email=email, password="CorrectHorse123!", is_staff=True)


def _question(topic: Topic, author: User, stem: str = "What is 1 + 1?") -> Question:
    return create_question(
        author,
        topic_id=topic.pk,
        stem=stem,
        options=[
            {"text": "1", "rationale": "Incorrect."},
            {"text": "2", "rationale": "Correct."},
        ],
        correct_answer_index=1,
        explanation="One plus one is two.",
        provenance="Original item.",
    )


def test_second_correct_choice_is_rejected():
    topic = _topic()
    question = _question(topic, _staff())

    with pytest.raises(IntegrityError):
        Choice.objects.create(
            question=question,
            text="Also two",
            rationale="Duplicate key.",
            is_correct=True,
            display_order=9,
        )


def test_difficulty_outside_one_to_five_is_rejected():
    topic = _topic()

    with pytest.raises(IntegrityError):
        Question.objects.create(
            topic=topic,
            stem="Out of range",
            stem_hash="a" * 64,
            difficulty=6,
            author=_staff(),
        )


def test_normalized_stem_hashes_match():
    topic = _topic()
    author = _staff()

    first = _question(topic, author, stem="What is 1 + 1?")
    second = _question(topic, author, stem="  what is   1 + 1?  ")

    assert first.stem_hash == second.stem_hash == stem_hash("What is 1 + 1?")


def test_open_flag_is_unique_per_reporter():
    topic = _topic()
    author = _staff()
    learner = User.objects.create_user(email="learner@example.com", password="CorrectHorse123!")
    question = _question(topic, author)

    ContentFlag.objects.create(question=question, reporter=learner, reason="typo")

    with pytest.raises(IntegrityError):
        ContentFlag.objects.create(question=question, reporter=learner, reason="unclear")
