from __future__ import annotations

from django.urls import path

from apps.practice.views import (
    PracticeSessionDetailView,
    PracticeSessionResultsView,
    PracticeSessionSaveAnswerView,
    PracticeSessionStartView,
    PracticeSessionSubmitView,
)

urlpatterns = [
    path("practice-sessions/", PracticeSessionStartView.as_view(), name="practice-list"),
    path(
        "practice-sessions/<uuid:id>/", PracticeSessionDetailView.as_view(), name="practice-detail"
    ),
    path(
        "practice-sessions/<uuid:id>/answers/<int:position>/",
        PracticeSessionSaveAnswerView.as_view(),
        name="practice-save-answer",
    ),
    path(
        "practice-sessions/<uuid:id>/submit/",
        PracticeSessionSubmitView.as_view(),
        name="practice-submit",
    ),
    path(
        "practice-sessions/<uuid:id>/results/",
        PracticeSessionResultsView.as_view(),
        name="practice-results",
    ),
]
