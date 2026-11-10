from __future__ import annotations

from django.db.models import Prefetch

from apps.catalog.models import Exam, ExamFamily, ExamVersion, Subject, Topic
from apps.catalog.serializers import exam_payload, family_payload


def exam_families() -> list[dict]:
    """Families → active exams → their newest active version."""
    families = ExamFamily.objects.prefetch_related(
        Prefetch(
            "exams",
            queryset=Exam.objects.filter(is_active=True).prefetch_related(
                Prefetch(
                    "versions",
                    queryset=ExamVersion.objects.filter(is_active=True),
                )
            ),
        )
    )
    result = []
    for family in families:
        exams = []
        for exam in family.exams.all():
            versions = list(exam.versions.all())
            exams.append(exam_payload(exam, versions[0] if versions else None))
        result.append(family_payload(family, exams))
    return result


def subjects_for_version(version_id) -> list[Subject]:
    return list(Subject.objects.filter(exam_version_id=version_id))


def topics_for_subject(subject_id) -> list[Topic]:
    return list(Topic.objects.filter(subject_id=subject_id))
