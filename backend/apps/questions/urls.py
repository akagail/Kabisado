from __future__ import annotations

from django.urls import path

from apps.questions.views import (
    FlagQueueView,
    QuestionCreateView,
    QuestionFlagCreateView,
    QuestionRetireView,
    QuestionReviewView,
    QuestionSubmitForReviewView,
    TopicQuestionsView,
)

urlpatterns = [
    path("questions/", QuestionCreateView.as_view(), name="questions-create"),
    path(
        "questions/<uuid:question_id>/submit-for-review/",
        QuestionSubmitForReviewView.as_view(),
        name="questions-submit-for-review",
    ),
    path(
        "questions/<uuid:question_id>/review/",
        QuestionReviewView.as_view(),
        name="questions-review",
    ),
    path(
        "questions/<uuid:question_id>/retire/",
        QuestionRetireView.as_view(),
        name="questions-retire",
    ),
    path(
        "questions/<uuid:question_id>/flags/",
        QuestionFlagCreateView.as_view(),
        name="questions-flags",
    ),
    path(
        "topics/<uuid:topic_id>/questions/",
        TopicQuestionsView.as_view(),
        name="topic-questions",
    ),
    path("admin/flags/", FlagQueueView.as_view(), name="admin-flags"),
]
