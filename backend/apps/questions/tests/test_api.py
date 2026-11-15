from __future__ import annotations

import uuid

import pytest
from django.core.management import call_command

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.questions import services
from apps.questions.models import Question

pytestmark = pytest.mark.django_db

CREATE = "/api/v1/questions/"
QUEUE = "/api/v1/admin/flags/"


def _topic() -> Topic:
    call_command("seed_cse_catalogue", force=True)
    return Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )


def _user(email: str, *, staff: bool = False) -> User:
    return User.objects.create_user(email=email, password="CorrectHorse123!", is_staff=staff)


def _payload(topic_obj: Topic, **overrides) -> dict:
    data = {
        "topic": str(topic_obj.pk),
        "stem": "What is 2 + 2?",
        "options": [
            {"text": "3", "rationale": "Incorrect."},
            {"text": "4", "rationale": "Correct."},
        ],
        "correct_answer_index": 1,
        "explanation": "Two plus two is four.",
        "provenance": "Original item.",
    }
    data.update(overrides)
    return data


def _create(api, topic: Topic, **overrides) -> dict:
    return api.post(CREATE, _payload(topic, **overrides), format="json").json()["question"]


def _published(topic: Topic, author: User, reviewer: User) -> Question:
    question = services.create_question(
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
    services.submit_for_review(author, question)
    services.review_question(reviewer, question, approve=True)
    return question


def test_endpoints_require_authentication(api, csrf):
    missing = uuid.uuid4()
    token = csrf()
    for response in (
        api.get(f"/api/v1/topics/{missing}/questions/"),
        api.get(QUEUE),
        api.post(CREATE, {}, format="json", HTTP_X_CSRFTOKEN=token),
        api.post(
            f"/api/v1/questions/{missing}/submit-for-review/",
            {},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        ),
        api.post(f"/api/v1/questions/{missing}/review/", {}, format="json", HTTP_X_CSRFTOKEN=token),
        api.post(f"/api/v1/questions/{missing}/retire/", {}, format="json", HTTP_X_CSRFTOKEN=token),
        api.post(f"/api/v1/questions/{missing}/flags/", {}, format="json", HTTP_X_CSRFTOKEN=token),
    ):
        assert response.status_code == 401


def test_learner_cannot_use_staff_endpoints(api):
    topic = _topic()
    learner = _user("learner@example.com")
    missing = uuid.uuid4()
    api.force_authenticate(user=learner)

    for response in (
        api.post(CREATE, _payload(topic), format="json"),
        api.post(f"/api/v1/questions/{missing}/submit-for-review/", {}, format="json"),
        api.post(f"/api/v1/questions/{missing}/review/", {}, format="json"),
        api.post(f"/api/v1/questions/{missing}/retire/", {}, format="json"),
        api.get(QUEUE),
    ):
        assert response.status_code == 403


def test_create_question_returns_staff_payload(api):
    topic = _topic()
    curator = _user("curator@example.com", staff=True)
    api.force_authenticate(user=curator)

    response = api.post(CREATE, _payload(topic), format="json")

    assert response.status_code == 201
    question = response.json()["question"]
    assert question["status"] == "draft"
    assert question["author_id"] == str(curator.pk)
    assert len(question["options"]) == 2
    assert [option["is_correct"] for option in question["options"]] == [False, True]
    assert question["explanation"] == "Two plus two is four."


def test_create_rejects_option_count(api):
    topic = _topic()
    api.force_authenticate(user=_user("curator@example.com", staff=True))

    response = api.post(
        CREATE,
        _payload(topic, options=[{"text": "Only", "rationale": "Alone."}]),
        format="json",
    )

    assert response.status_code == 400
    assert "options" in response.json()["error"]["fields"]


def test_unknown_topic_and_question_return_not_found(api):
    topic = _topic()
    curator = _user("curator@example.com", staff=True)
    learner = _user("learner@example.com")
    missing = uuid.uuid4()

    api.force_authenticate(user=curator)
    assert api.post(CREATE, _payload(topic, topic=str(missing)), format="json").status_code == 404

    api.force_authenticate(user=learner)
    assert api.get(f"/api/v1/topics/{missing}/questions/").status_code == 404
    response = api.post(f"/api/v1/questions/{missing}/flags/", {"reason": "typo"}, format="json")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_submit_and_approve_publishes_for_learners(api):
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")

    api.force_authenticate(user=author)
    question = _create(api, topic)
    assert (
        api.post(
            f"/api/v1/questions/{question['id']}/submit-for-review/", {}, format="json"
        ).status_code
        == 200
    )

    api.force_authenticate(user=reviewer)
    response = api.post(
        f"/api/v1/questions/{question['id']}/review/", {"approve": True}, format="json"
    )
    assert response.status_code == 200
    assert response.json()["status"] == "published"

    api.force_authenticate(user=learner)
    listed = api.get(f"/api/v1/topics/{topic.pk}/questions/")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [question["id"]]


def test_review_without_explanation_returns_validation_error(api):
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)

    api.force_authenticate(user=author)
    question = _create(api, topic, explanation="", provenance="")
    api.post(f"/api/v1/questions/{question['id']}/submit-for-review/", {}, format="json")

    api.force_authenticate(user=reviewer)
    response = api.post(
        f"/api/v1/questions/{question['id']}/review/", {"approve": True}, format="json"
    )

    assert response.status_code == 400
    fields = response.json()["error"]["fields"]
    assert "explanation" in fields
    assert "provenance" in fields


def test_submit_twice_returns_conflict(api):
    topic = _topic()
    curator = _user("curator@example.com", staff=True)
    api.force_authenticate(user=curator)
    question = _create(api, topic)

    first = api.post(f"/api/v1/questions/{question['id']}/submit-for-review/", {}, format="json")
    second = api.post(f"/api/v1/questions/{question['id']}/submit-for-review/", {}, format="json")

    assert first.status_code == 200
    assert second.status_code == 409


def test_duplicate_open_flag_returns_conflict(api):
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")
    question = _published(topic, author, reviewer)
    api.force_authenticate(user=learner)

    first = api.post(f"/api/v1/questions/{question.pk}/flags/", {"reason": "typo"}, format="json")
    second = api.post(
        f"/api/v1/questions/{question.pk}/flags/", {"reason": "unclear"}, format="json"
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_learner_list_hides_answers_and_drafts(api):
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")
    published = _published(topic, author, reviewer)
    services.create_question(
        author,
        topic_id=topic.pk,
        stem="Hidden draft",
        options=[
            {"text": "A", "rationale": "No."},
            {"text": "B", "rationale": "Yes."},
        ],
        correct_answer_index=0,
    )

    api.force_authenticate(user=learner)
    response = api.get(f"/api/v1/topics/{topic.pk}/questions/")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [str(published.pk)]
    option = response.json()[0]["options"][0]
    assert "is_correct" not in option
    assert "rationale" not in option
    assert "explanation" not in response.json()[0]
    assert "provenance" not in response.json()[0]


def test_flag_queue_lists_open_flags_for_staff(api):
    topic = _topic()
    author = _user("author@example.com", staff=True)
    reviewer = _user("reviewer@example.com", staff=True)
    learner = _user("learner@example.com")
    question = _published(topic, author, reviewer)
    api.force_authenticate(user=learner)
    api.post(f"/api/v1/questions/{question.pk}/flags/", {"reason": "typo"}, format="json")

    api.force_authenticate(user=reviewer)
    response = api.get(QUEUE)

    assert response.status_code == 200
    assert len(response.json()) == 1
    item = response.json()[0]
    assert item["flag"]["reason"] == "typo"
    assert item["flag"]["status"] == "open"
    assert item["reporter"]["id"] == str(learner.pk)
    assert item["question"]["id"] == str(question.pk)
