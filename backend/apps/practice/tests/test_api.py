from __future__ import annotations

import uuid

import pytest
from django.core.management import call_command
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.core.models import AuditEvent
from apps.practice.models import PracticeSession
from apps.questions.models import Question
from apps.questions.services import create_question, review_question, submit_for_review

pytestmark = pytest.mark.django_db

BASE = "/api/v1/practice-sessions/"


def _topic():
    call_command("seed_cse_catalogue", force=True)
    return Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )


def _user(email="learner@example.com", staff=True):
    return User.objects.create_user(email=email, password="CorrectHorse123!", is_staff=staff)


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


def _start_session(api, user, topic, mode="untimed"):
    count = _published_question_count(topic)
    payload = {"topic": str(topic.pk), "mode": mode, "size": count}
    response = api.post(BASE, payload, format="json")
    assert response.status_code == 201
    return response.json()


def test_start_session_requires_authentication(api):
    topic = _topic()
    response = api.post(BASE, {"topic": str(topic.pk), "mode": "untimed", "size": 1}, format="json")
    # The CSRF-enforcing authentication class returns 403 for an unauthenticated
    # POST without a CSRF token; 401 is returned once the token is present.
    assert response.status_code == 403


def test_start_session_returns_session(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)

    data = _start_session(api, user, topic)
    assert data["mode"] == "untimed"
    assert data["status"] == "in_progress"
    assert len(data["items"]) == _published_question_count(topic)
    assert data["items"][0]["position"] == 0
    assert "snapshot_options" not in data  # serializer exposes question dict


def test_start_session_invalid_topic_returns_404(api):
    user = _user()
    api.force_authenticate(user=user)
    response = api.post(
        BASE,
        {"topic": str(uuid.uuid4()), "mode": "untimed", "size": 1},
        format="json",
    )
    assert response.status_code == 404


def test_start_session_invalid_mode_returns_400(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    response = api.post(
        BASE,
        {"topic": str(topic.pk), "mode": "invalid", "size": 1},
        format="json",
    )
    assert response.status_code == 400


def test_get_session_returns_own_session(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    response = api.get(f"{BASE}{session['id']}/")
    assert response.status_code == 200
    assert response.json()["id"] == session["id"]


def test_get_session_other_user_returns_404(api):
    topic = _topic()
    user = _user()
    other = _user("other@example.com")
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    api.force_authenticate(user=other)
    response = api.get(f"{BASE}{session['id']}/")
    assert response.status_code == 404


def test_session_payload_hides_correctness_before_submit(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    response = api.get(f"{BASE}{session['id']}/")
    options = response.json()["items"][0]["question"]["options"]
    assert all("is_correct" not in option for option in options)


def test_save_answer_after_expiry_returns_409(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic, mode="timed")

    PracticeSession.objects.filter(pk=session["id"]).update(
        expires_at=timezone.now() - timezone.timedelta(seconds=1)
    )
    response = api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(uuid.uuid4())},
        format="json",
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "session_expired"


def test_expired_session_detail_auto_submits(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic, mode="timed")

    PracticeSession.objects.filter(pk=session["id"]).update(
        expires_at=timezone.now() - timezone.timedelta(seconds=1)
    )
    response = api.get(f"{BASE}{session['id']}/")
    assert response.status_code == 200
    assert response.json()["status"] == "submitted"
    assert response.json()["score_total"] == _published_question_count(topic)


def test_saved_answer_survives_refetch(api):
    topic = _topic()
    user = _user()
    question = _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)
    choice = question.choices.get(is_correct=True)

    api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(choice.id)},
        format="json",
    )
    response = api.get(f"{BASE}{session['id']}/")
    assert response.json()["items"][0]["saved_answer"] == {"selected_option_id": str(choice.id)}


def test_save_answer_and_submit(api):
    topic = _topic()
    user = _user()
    question = _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    choice = question.choices.get(is_correct=True)
    response = api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(choice.id)},
        format="json",
    )
    assert response.status_code == 204

    response = api.post(f"{BASE}{session['id']}/submit/", {}, format="json")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "submitted"
    assert data["score_correct"] == 1
    assert data["score_total"] == _published_question_count(topic)


def test_submit_is_idempotent(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    first = api.post(f"{BASE}{session['id']}/submit/", {}, format="json")
    second = api.post(f"{BASE}{session['id']}/submit/", {}, format="json")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["score_correct"] == second.json()["score_correct"]


def test_results_after_submit(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)
    api.post(f"{BASE}{session['id']}/submit/", {}, format="json")

    response = api.get(f"{BASE}{session['id']}/results/")
    assert response.status_code == 200
    data = response.json()
    assert data["score_total"] == _published_question_count(topic)
    assert "items" in data


def test_results_before_submit_forbidden(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    response = api.get(f"{BASE}{session['id']}/results/")
    assert response.status_code == 403


def test_history_returns_own_sessions(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    _start_session(api, user, topic)

    response = api.get(BASE)
    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_history_excludes_other_users(api):
    topic = _topic()
    user = _user()
    other = _user("other@example.com")
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    _start_session(api, user, topic)

    api.force_authenticate(user=other)
    response = api.get(BASE)
    assert response.status_code == 200
    assert response.json()["results"] == []


def test_save_answer_can_change_choice(api):
    topic = _topic()
    user = _user()
    question = _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)
    wrong = question.choices.get(is_correct=False)
    right = question.choices.get(is_correct=True)

    api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(wrong.id)},
        format="json",
    )
    api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(right.id)},
        format="json",
    )

    data = api.get(f"{BASE}{session['id']}/").json()
    assert data["items"][0]["saved_answer"]["selected_option_id"] == str(right.id)

    submitted = api.post(f"{BASE}{session['id']}/submit/", {}, format="json").json()
    assert submitted["score_correct"] == 1


def test_save_answer_writes_an_audit_event(api):
    topic = _topic()
    user = _user()
    question = _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)
    choice = question.choices.first()

    api.put(
        f"{BASE}{session['id']}/answers/0/",
        {"selected_option_id": str(choice.id)},
        format="json",
    )

    assert (
        AuditEvent.objects.filter(
            actor=user, action=AuditEvent.Action.PRACTICE_ANSWER_SAVED
        ).count()
        == 1
    )


def test_results_view_writes_an_audit_event(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)
    api.post(f"{BASE}{session['id']}/submit/", {}, format="json")

    api.get(f"{BASE}{session['id']}/results/")

    assert (
        AuditEvent.objects.filter(
            actor=user, action=AuditEvent.Action.PRACTICE_RESULT_VIEWED
        ).count()
        == 1
    )


def test_repeated_submit_writes_one_submit_audit_event(api):
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)
    session = _start_session(api, user, topic)

    api.post(f"{BASE}{session['id']}/submit/", {}, format="json")
    api.post(f"{BASE}{session['id']}/submit/", {}, format="json")

    assert (
        AuditEvent.objects.filter(
            actor=user, action=AuditEvent.Action.PRACTICE_SESSION_SUBMITTED
        ).count()
        == 1
    )


def test_history_is_paginated(api):
    topic = _topic()
    user = _user()
    api.force_authenticate(user=user)
    for _ in range(25):
        PracticeSession.objects.create(
            user=user, exam_version=topic.subject.exam_version, mode="untimed"
        )

    first = api.get(BASE).json()

    assert first["count"] == 25
    assert len(first["results"]) == 20
    assert first["next"]

    second = api.get(BASE, {"page": 2}).json()
    assert len(second["results"]) == 5
    assert second["previous"]


def test_timed_limit_comes_from_settings(api, settings):
    settings.PRACTICE_TIMED_LIMIT_SECONDS = 120
    topic = _topic()
    user = _user()
    _create_published_question(topic, user)
    api.force_authenticate(user=user)

    session = _start_session(api, user, topic, mode="timed")

    assert session["time_limit_seconds"] == 120
