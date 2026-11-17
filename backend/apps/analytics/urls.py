from __future__ import annotations

from django.urls import path

from apps.analytics.views import AnalyticsSummaryView, AnalyticsTopicsView

urlpatterns = [
    path("analytics/summary/", AnalyticsSummaryView.as_view(), name="analytics-summary"),
    path("analytics/topics/", AnalyticsTopicsView.as_view(), name="analytics-topics"),
]
