from __future__ import annotations

from django.urls import path

from apps.catalog.views import (
    ExamListView,
    ExamVersionSubjectsView,
    SubjectTopicsView,
    TopicDetailView,
)

urlpatterns = [
    path("exams/", ExamListView.as_view(), name="catalog-exams"),
    path(
        "exam-versions/<uuid:version_id>/subjects/",
        ExamVersionSubjectsView.as_view(),
        name="catalog-version-subjects",
    ),
    path(
        "subjects/<uuid:subject_id>/topics/",
        SubjectTopicsView.as_view(),
        name="catalog-subject-topics",
    ),
    path("topics/<uuid:topic_id>/", TopicDetailView.as_view(), name="catalog-topic"),
]
