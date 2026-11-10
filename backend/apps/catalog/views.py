from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog import selectors
from apps.catalog.models import ExamVersion, Subject, Topic
from apps.catalog.serializers import (
    ExamFamilyListSerializer,
    SubjectSerializer,
    TopicSerializer,
    subject_payload,
    topic_payload,
)

_NOT_FOUND = {
    ExamVersion: "Exam version not found.",
    Subject: "Subject not found.",
    Topic: "Topic not found.",
}


def _require(model, **lookup):
    try:
        return model.objects.get(**lookup)
    except model.DoesNotExist as exc:
        raise NotFound(_NOT_FOUND[model]) from exc


class ExamListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: ExamFamilyListSerializer})
    def get(self, request):
        return Response({"exam_families": selectors.exam_families()})


class ExamVersionSubjectsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: SubjectSerializer(many=True)})
    def get(self, request, version_id):
        version = _require(ExamVersion, pk=version_id, is_active=True)
        subjects = selectors.subjects_for_version(version.pk)
        return Response([subject_payload(subject) for subject in subjects])


class SubjectTopicsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: TopicSerializer(many=True)})
    def get(self, request, subject_id):
        subject = _require(Subject, pk=subject_id)
        topics = selectors.topics_for_subject(subject.pk)
        return Response([topic_payload(topic) for topic in topics])


class TopicDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: TopicSerializer})
    def get(self, request, topic_id):
        topic = _require(Topic, pk=topic_id)
        return Response(topic_payload(topic))
