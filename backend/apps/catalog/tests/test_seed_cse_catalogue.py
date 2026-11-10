from __future__ import annotations

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError

from apps.catalog.models import Exam, ExamFamily, ExamVersion, Subject, Topic

pytestmark = pytest.mark.django_db


def _seed():
    call_command("seed_cse_catalogue", force=True)


def test_seed_creates_the_official_tree():
    _seed()

    professional = Exam.objects.get(slug="cse-professional")
    subjects = list(professional.versions.get(slug="2027-bulletin").subjects.all())
    assert [subject.slug for subject in subjects] == [
        "general-information",
        "verbal-ability",
        "numerical-ability",
        "analytical-ability",
    ]
    assert subjects[0].topics.count() == 4

    subprofessional = Exam.objects.get(slug="cse-subprofessional")
    assert list(
        subprofessional.versions.get(slug="2027-bulletin").subjects.values_list("slug", flat=True)
    ) == ["general-information", "verbal-ability", "numerical-ability", "clerical-ability"]


def test_seed_is_idempotent():
    _seed()
    counts = (
        ExamFamily.objects.count(),
        Exam.objects.count(),
        Subject.objects.count(),
        Topic.objects.count(),
    )

    _seed()

    assert (
        ExamFamily.objects.count(),
        Exam.objects.count(),
        Subject.objects.count(),
        Topic.objects.count(),
    ) == counts


def test_seed_requires_force_when_debug_is_off(settings):
    settings.DEBUG = False

    with pytest.raises(CommandError):
        call_command("seed_cse_catalogue")


def test_version_records_official_source_and_leaves_unverified_facts_null():
    _seed()

    version = ExamVersion.objects.get(exam__slug="cse-professional", slug="2027-bulletin")

    assert version.source_url.startswith("https://csc.gov.ph/")
    assert version.published_at.isoformat() == "2026-10-21"
    assert float(version.passing_rate) == 80.0
    # Item count and time limit are not published for this version.
    assert version.item_count is None
    assert version.time_limit_seconds is None


def test_root_topic_slug_is_unique_within_a_subject():
    _seed()
    subject = Subject.objects.get(
        exam_version__exam__slug="cse-professional", slug="verbal-ability"
    )
    existing = subject.topics.get(slug="word-meaning")

    with pytest.raises(IntegrityError):
        Topic.objects.create(subject=subject, slug=existing.slug, name="Duplicate")


def test_same_topic_slug_may_repeat_across_subjects():
    _seed()
    numerical = Subject.objects.get(
        exam_version__exam__slug="cse-professional", slug="numerical-ability"
    )
    administrative = Subject.objects.get(
        exam_version__exam__slug="cse-subprofessional", slug="numerical-ability"
    )

    Topic.objects.create(subject=numerical, slug="rates", name="Rates")
    Topic.objects.create(subject=administrative, slug="rates", name="Rates")

    assert Topic.objects.filter(slug="rates").count() == 2
