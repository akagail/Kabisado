from __future__ import annotations

import uuid

import pytest
from django.core.management import call_command
from django.utils import timezone

from apps.accounts.models import Profile, User
from apps.catalog.models import ExamVersion, Topic
from apps.practice.models import AttemptAnswer, PracticeSession, SessionItem
from apps.questions.models import Question

pytestmark = pytest.mark.django_db

SUMMARY = "/api/v1/analytics/summary/"
TOPICS = "/api/v1/analytics/topics/"


@pytest.fixture
def catalogue():
    call_command("seed_cse_catalogue", force=True)
    return ExamVersion.objects.get(exam__slug="cse-professional")


def _topic(version, slug):
    return Topic.objects.get(subject__exam_version=version, slug=slug)


def _user(email, target_exam):
    user = User.objects.create_user(email=email, password="CorrectHorse123!")
    Profile.objects.filter(user=user).update(target_exam=target_exam)
    return user


def _session(user, version, answers, status=PracticeSession.Status.SUBMITTED):
    session = PracticeSession.objects.create(
        user=user,
        exam_version=version,
        mode=PracticeSession.Mode.UNTIMED,
        status=status,
        submitted_at=timezone.now() if status == PracticeSession.Status.SUBMITTED else None,
    )
    for index, (topic, is_correct) in enumerate(answers):
        question = Question.objects.create(
            topic=topic,
            stem=f"Question {index}",
            stem_hash=uuid.uuid4().hex,
            author=user,
            status=Question.Status.PUBLISHED,
        )
        item = SessionItem.objects.create(
            session=session,
            question=question,
            display_order=index,
            snapshot_stem=question.stem,
            snapshot_options=[],
            snapshot_explanation="",
            snapshot_provenance="",
            snapshot_difficulty=1,
        )
        AttemptAnswer.objects.create(session_item=item, is_correct=is_correct)
    return session


def _by_slug(rows, slug):
    return next(row for row in rows if row["topic"]["slug"] == slug)


def test_summary_aggregates_by_subject(api, catalogue):
    user = _user("learner@example.com", catalogue.exam)
    _session(
        user,
        catalogue,
        [
            (_topic(catalogue, "word-meaning"), True),
            (_topic(catalogue, "word-meaning"), False),
            (_topic(catalogue, "basic-operations"), True),
        ],
    )
    api.force_authenticate(user=user)

    response = api.get(SUMMARY)

    assert response.status_code == 200
    subjects = {row["subject"]["slug"]: row for row in response.json()["subjects"]}
    assert subjects["verbal-ability"]["attempts"] == 2
    assert subjects["verbal-ability"]["accuracy"] == 50.0
    assert subjects["numerical-ability"]["attempts"] == 1
    assert subjects["numerical-ability"]["accuracy"] == 100.0


def test_topics_apply_the_weak_topic_boundaries(api, catalogue):
    user = _user("learner@example.com", catalogue.exam)
    _session(
        user,
        catalogue,
        [(_topic(catalogue, "word-meaning"), True)] * 7
        + [(_topic(catalogue, "word-meaning"), False)] * 3
        + [(_topic(catalogue, "sentence-completion"), True)] * 2
        + [(_topic(catalogue, "sentence-completion"), False)]
        + [(_topic(catalogue, "error-recognition"), False)] * 2,
    )
    api.force_authenticate(user=user)

    rows = api.get(TOPICS).json()["topics"]

    at_threshold = _by_slug(rows, "word-meaning")
    assert at_threshold["accuracy"] == 70.0
    assert at_threshold["weak_topic"] is False
    assert at_threshold["weak_reason"] is None

    below_threshold = _by_slug(rows, "sentence-completion")
    assert below_threshold["accuracy"] == 66.67
    assert below_threshold["attempts"] == 3
    assert below_threshold["weak_topic"] is True
    assert below_threshold["weak_reason"]

    too_few_attempts = _by_slug(rows, "error-recognition")
    assert too_few_attempts["attempts"] == 2
    assert too_few_attempts["weak_topic"] is False


def test_threshold_is_configurable(api, catalogue, settings):
    settings.ANALYTICS_WEAK_TOPIC_ACCURACY_THRESHOLD = 60.0
    user = _user("learner@example.com", catalogue.exam)
    _session(
        user,
        catalogue,
        [(_topic(catalogue, "word-meaning"), True)] * 2
        + [(_topic(catalogue, "word-meaning"), False)],
    )
    api.force_authenticate(user=user)

    row = api.get(TOPICS).json()["topics"][0]

    assert row["weak_topic"] is False


def test_minimum_attempts_is_configurable(api, catalogue, settings):
    settings.ANALYTICS_WEAK_TOPIC_MIN_ATTEMPTS = 5
    user = _user("learner@example.com", catalogue.exam)
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), False)] * 3)
    api.force_authenticate(user=user)

    row = api.get(TOPICS).json()["topics"][0]

    assert row["weak_topic"] is False


def test_empty_state_returns_empty_lists(api, catalogue):
    user = _user("learner@example.com", catalogue.exam)
    api.force_authenticate(user=user)

    assert api.get(SUMMARY).json() == {"subjects": []}
    assert api.get(TOPICS).json() == {"topics": []}


def test_only_submitted_sessions_count(api, catalogue):
    user = _user("learner@example.com", catalogue.exam)
    _session(
        user,
        catalogue,
        [(_topic(catalogue, "word-meaning"), True)],
        status=PracticeSession.Status.IN_PROGRESS,
    )
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), False)])
    api.force_authenticate(user=user)

    row = api.get(TOPICS).json()["topics"][0]

    assert row["attempts"] == 1
    assert row["accuracy"] == 0.0


def test_other_users_answers_are_excluded(api, catalogue):
    user = _user("learner@example.com", catalogue.exam)
    other = _user("other@example.com", catalogue.exam)
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), True)])
    _session(other, catalogue, [(_topic(catalogue, "word-meaning"), False)] * 3)
    api.force_authenticate(user=user)

    row = api.get(TOPICS).json()["topics"][0]

    assert row["attempts"] == 1
    assert row["accuracy"] == 100.0


def test_progress_is_scoped_to_the_target_exam(api, catalogue):
    subprofessional = ExamVersion.objects.get(exam__slug="cse-subprofessional")
    user = _user("learner@example.com", catalogue.exam)
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), True)])
    _session(user, subprofessional, [(_topic(subprofessional, "spelling"), False)] * 3)
    api.force_authenticate(user=user)

    rows = api.get(TOPICS).json()["topics"]

    assert [row["topic"]["slug"] for row in rows] == ["word-meaning"]

    Profile.objects.filter(user=user).update(target_exam=subprofessional.exam)
    rows = api.get(TOPICS).json()["topics"]
    assert [row["topic"]["slug"] for row in rows] == ["spelling"]


def test_no_target_exam_returns_empty(api, catalogue):
    user = _user("learner@example.com", None)
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), True)])
    api.force_authenticate(user=user)

    assert api.get(TOPICS).json() == {"topics": []}


def test_endpoints_require_authentication(api):
    assert api.get(SUMMARY).status_code == 401
    assert api.get(TOPICS).status_code == 401


def test_query_count_is_bounded(api, catalogue, django_assert_max_num_queries):
    user = _user("learner@example.com", catalogue.exam)
    _session(user, catalogue, [(_topic(catalogue, "word-meaning"), True)] * 3)
    api.force_authenticate(user=user)

    with django_assert_max_num_queries(2):
        assert api.get(SUMMARY).status_code == 200
    with django_assert_max_num_queries(2):
        assert api.get(TOPICS).status_code == 200
