from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analytics import selectors
from apps.analytics.serializers import SubjectAnalyticsSerializer, TopicAnalyticsSerializer


class AnalyticsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: SubjectAnalyticsSerializer})
    def get(self, request):
        payload = {"subjects": selectors.subject_analytics(request.user)}
        return Response(SubjectAnalyticsSerializer(payload).data)


class AnalyticsTopicsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: TopicAnalyticsSerializer})
    def get(self, request):
        payload = {"topics": selectors.topic_analytics(request.user)}
        return Response(TopicAnalyticsSerializer(payload).data)
