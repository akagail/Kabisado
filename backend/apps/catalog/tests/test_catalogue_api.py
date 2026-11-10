from __future__ import annotations

import uuid

import pytest
from django.core.management import call_command

from apps.catalog.models import ExamVersion, Subject, Topic

pytestmark = pytest.mark.django_db

VALID_PASSWORD = "CorrectHorse123!"
REGISTER = "/api/v1/auth/register/"
EXAMS = "/api/v1/exams/"


def _logged_in(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )


@pytest.fixture
def catalogue(api, csrf):
    call_command("seed_cse_catalogue", force=True)
    _logged_in(api, csrf)
    return api


def _professional_version() -> ExamVersion:
    return ExamVersion.objects.get(exam__slug="cse-professional", slug="2027-bulletin")


def test_catalogue_requires_authentication(api):
    for path in (
        EXAMS,
        f"/api/v1/exam-versions/{uuid.uuid4()}/subjects/",
        f"/api/v1/subjects/{uuid.uuid4()}/topics/",
        f"/api/v1/topics/{uuid.uuid4()}/",
    ):
        assert api.get(path).status_code == 401


def test_exams_returns_families_with_exams_and_current_version(catalogue):
    response = catalogue.get(EXAMS)

    assert response.status_code == 200
    families = response.json()["exam_families"]
    assert [family["slug"] for family in families] == ["cse"]
    exams = families[0]["exams"]
    assert [exam["slug"] for exam in exams] == ["cse-professional", "cse-subprofessional"]
    assert exams[0]["level"] == "professional"
    assert exams[0]["current_version"]["slug"] == "2027-bulletin"
    assert exams[0]["current_version"]["published_at"] == "2026-10-21"


def test_subjects_are_listed_in_official_order(catalogue):
    response = catalogue.get(f"/api/v1/exam-versions/{_professional_version().pk}/subjects/")

    assert response.status_code == 200
    assert [subject["slug"] for subject in response.json()] == [
        "general-information",
        "verbal-ability",
        "numerical-ability",
        "analytical-ability",
    ]
    assert response.json()[0]["display_order"] == 0


def test_topics_include_accuracy_and_attempt_placeholders(catalogue):
    subject = Subject.objects.get(exam_version=_professional_version(), slug="verbal-ability")

    response = catalogue.get(f"/api/v1/subjects/{subject.pk}/topics/")

    assert response.status_code == 200
    topics = response.json()
    assert [topic["slug"] for topic in topics][:2] == ["word-meaning", "sentence-completion"]
    assert topics[0]["accuracy"] is None
    assert topics[0]["attempts"] == 0
    assert topics[0]["weak_topic"] is False


def test_topic_detail_returns_a_single_topic(catalogue):
    topic = Topic.objects.get(subject__slug="clerical-ability", slug="filing")

    response = catalogue.get(f"/api/v1/topics/{topic.pk}/")

    assert response.status_code == 200
    assert response.json()["name"] == "Filing"


def test_unknown_catalogue_ids_return_not_found(catalogue):
    missing = uuid.uuid4()

    for path in (
        f"/api/v1/exam-versions/{missing}/subjects/",
        f"/api/v1/subjects/{missing}/topics/",
        f"/api/v1/topics/{missing}/",
    ):
        response = catalogue.get(path)
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "not_found"
