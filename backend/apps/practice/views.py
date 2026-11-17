from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import DefaultPagination
from apps.practice import services
from apps.practice.serializers import (
    PracticeSessionDetailSerializer,
    PracticeSessionHistoryPageSerializer,
    PracticeSessionHistorySerializer,
    PracticeSessionResultsSerializer,
    PracticeSessionSaveAnswerSerializer,
    PracticeSessionStartSerializer,
    PracticeSessionSubmitSerializer,
)


class PracticeSessionStartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PracticeSessionStartSerializer, responses={201: PracticeSessionDetailSerializer}
    )
    def post(self, request):
        serializer = PracticeSessionStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        session = services.start_session(
            request.user,
            mode=data["mode"],
            topic_identifier=data["topic"],
            size=data.get("size", 20),
        )
        return Response(
            PracticeSessionDetailSerializer(session).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(responses=PracticeSessionHistoryPageSerializer)
    def get(self, request):
        queryset = services.get_session_history(request.user)
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PracticeSessionHistorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PracticeSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PracticeSessionDetailSerializer)
    def get(self, request, id):
        session = services.get_session(request.user, id)
        return Response(PracticeSessionDetailSerializer(session).data)


class PracticeSessionSaveAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=PracticeSessionSaveAnswerSerializer, responses={204: None})
    def put(self, request, id, position):
        serializer = PracticeSessionSaveAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.save_answer(
            request.user, id, position, serializer.validated_data.get("selected_option_id")
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class PracticeSessionSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: PracticeSessionSubmitSerializer})
    def post(self, request, id):
        session = services.submit_session(request.user, id)
        return Response(PracticeSessionSubmitSerializer(session).data)


class PracticeSessionResultsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PracticeSessionResultsSerializer)
    def get(self, request, id):
        results = services.get_session_results(request.user, id)
        return Response(results)
