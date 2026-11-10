from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Topic
from apps.questions import selectors, services
from apps.questions.models import Question
from apps.questions.serializers import (
    ContentFlagEnvelopeSerializer,
    FlagCreateSerializer,
    FlagQueueItemSerializer,
    LearnerQuestionSerializer,
    QuestionCreateSerializer,
    QuestionEnvelopeSerializer,
    QuestionRetireSerializer,
    QuestionReviewSerializer,
    QuestionStatusSerializer,
    flag_payload,
    question_payload,
)


class SizePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 100


def _question_or_404(question_id) -> Question:
    question = (
        Question.objects.select_related("author", "reviewer")
        .prefetch_related("choices")
        .filter(pk=question_id)
        .first()
    )
    if question is None:
        raise NotFound("Item not found.")
    return question


class QuestionCreateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(request=QuestionCreateSerializer, responses={201: QuestionEnvelopeSerializer})
    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        topic_id = data.pop("topic")
        question = services.create_question(request.user, topic_id=topic_id, **data)
        question = _question_or_404(question.pk)
        return Response(
            {"question": question_payload(question, include_answer=True)},
            status=status.HTTP_201_CREATED,
        )


class QuestionSubmitForReviewView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(request=None, responses={200: QuestionStatusSerializer})
    def post(self, request, question_id):
        question = services.submit_for_review(request.user, _question_or_404(question_id))
        return Response(
            {
                "question": question_payload(question, include_answer=True),
                "status": question.status,
            }
        )


class QuestionReviewView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(request=QuestionReviewSerializer, responses={200: QuestionStatusSerializer})
    def post(self, request, question_id):
        serializer = QuestionReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = services.review_question(
            request.user,
            _question_or_404(question_id),
            **serializer.validated_data,
        )
        return Response(
            {
                "question": question_payload(question, include_answer=True),
                "status": question.status,
            }
        )


class QuestionRetireView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(request=QuestionRetireSerializer, responses={200: QuestionStatusSerializer})
    def post(self, request, question_id):
        serializer = QuestionRetireSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = services.retire_question(
            request.user, _question_or_404(question_id), **serializer.validated_data
        )
        return Response(
            {
                "question": question_payload(question, include_answer=True),
                "status": question.status,
            }
        )


class TopicQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: LearnerQuestionSerializer(many=True)})
    def get(self, request, topic_id):
        if not Topic.objects.filter(pk=topic_id).exists():
            raise NotFound("Topic not found.")
        queryset = selectors.published_questions_for_topic(topic_id)
        paginator = SizePagination()
        page = paginator.paginate_queryset(queryset, request) or []
        return Response([question_payload(question, include_answer=False) for question in page])


class QuestionFlagCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=FlagCreateSerializer, responses={201: ContentFlagEnvelopeSerializer})
    def post(self, request, question_id):
        serializer = FlagCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = _question_or_404(question_id)
        flag = services.create_flag(request.user, question, **serializer.validated_data)
        return Response({"flag": flag_payload(flag)}, status=status.HTTP_201_CREATED)


class FlagQueueView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(responses={200: FlagQueueItemSerializer(many=True)})
    def get(self, request):
        paginator = SizePagination()
        page = paginator.paginate_queryset(selectors.open_flags(), request) or []
        return Response(
            [
                {
                    "flag": flag_payload(flag),
                    "reporter": {"id": str(flag.reporter_id)} if flag.reporter_id else None,
                    "question": {
                        "id": str(flag.question_id),
                        "stem": flag.question.stem,
                        "status": flag.question.status,
                    },
                }
                for flag in page
            ]
        )
