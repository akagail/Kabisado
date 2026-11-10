from __future__ import annotations

from rest_framework import serializers

from apps.catalog.models import Exam, ExamFamily, ExamVersion, Subject, Topic


def version_payload(version: ExamVersion) -> dict:
    return {
        "id": str(version.pk),
        "slug": version.slug,
        "label": version.label,
        "source_url": version.source_url,
        "published_at": version.published_at.isoformat(),
        "passing_rate": float(version.passing_rate) if version.passing_rate is not None else None,
    }


def exam_payload(exam: Exam, current_version: ExamVersion | None) -> dict:
    return {
        "id": str(exam.pk),
        "slug": exam.slug,
        "name": exam.name,
        "level": exam.level,
        # Additive to SPEC-0002 §8: the client needs a version id to list subjects.
        "current_version": version_payload(current_version) if current_version else None,
    }


def family_payload(family: ExamFamily, exams: list[dict]) -> dict:
    return {"id": str(family.pk), "slug": family.slug, "name": family.name, "exams": exams}


def subject_payload(subject: Subject) -> dict:
    return {
        "id": str(subject.pk),
        "slug": subject.slug,
        "name": subject.name,
        "display_order": subject.display_order,
    }


def topic_payload(topic: Topic) -> dict:
    # shortcut: accuracy/attempts need practice responses (KAB-104); null until then.
    return {
        "id": str(topic.pk),
        "slug": topic.slug,
        "name": topic.name,
        "display_order": topic.display_order,
        "accuracy": None,
        "attempts": 0,
        "weak_topic": False,
    }


class ExamVersionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    label = serializers.CharField()
    source_url = serializers.URLField()
    published_at = serializers.DateField()
    passing_rate = serializers.FloatField(allow_null=True)


class ExamSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()
    level = serializers.CharField()
    current_version = ExamVersionSerializer(allow_null=True)


class ExamFamilySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()
    exams = ExamSerializer(many=True)


class ExamFamilyListSerializer(serializers.Serializer):
    exam_families = ExamFamilySerializer(many=True)


class SubjectSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()
    display_order = serializers.IntegerField()


class TopicSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()
    display_order = serializers.IntegerField()
    accuracy = serializers.FloatField(allow_null=True)
    attempts = serializers.IntegerField()
    weak_topic = serializers.BooleanField()
