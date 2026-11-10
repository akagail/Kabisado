from __future__ import annotations

from apps.questions.models import ContentFlag, Question


def published_questions_for_topic(topic_id):
    return (
        Question.objects.filter(topic_id=topic_id, status=Question.Status.PUBLISHED)
        .prefetch_related("choices")
        .order_by("id")
    )


def open_flags():
    return ContentFlag.objects.filter(status=ContentFlag.Status.OPEN).select_related(
        "question", "reporter"
    )
