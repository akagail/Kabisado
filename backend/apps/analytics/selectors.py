from __future__ import annotations

from django.conf import settings
from django.db.models import Count, F, Q

from apps.accounts.models import Profile
from apps.practice.models import AttemptAnswer, PracticeSession


def _rule():
    return (
        settings.ANALYTICS_WEAK_TOPIC_MIN_ATTEMPTS,
        float(settings.ANALYTICS_WEAK_TOPIC_ACCURACY_THRESHOLD),
    )


def _submitted_answers(actor):
    """Answered items from the actor's submitted sessions for their target exam."""
    target_exam_id = (
        Profile.objects.filter(user=actor).values_list("target_exam_id", flat=True).first()
    )
    if target_exam_id is None:
        return AttemptAnswer.objects.none()
    return AttemptAnswer.objects.filter(
        session_item__session__user=actor,
        session_item__session__status=PracticeSession.Status.SUBMITTED,
        session_item__session__exam_version__exam_id=target_exam_id,
        is_correct__isnull=False,
    )


def _accuracy(correct: int, attempts: int) -> float:
    return round(correct * 100 / attempts, 2)


def subject_analytics(actor) -> list[dict]:
    rows = (
        _submitted_answers(actor)
        .values(
            subject_id=F("session_item__question__topic__subject_id"),
            slug=F("session_item__question__topic__subject__slug"),
            name=F("session_item__question__topic__subject__name"),
            display_order=F("session_item__question__topic__subject__display_order"),
        )
        .annotate(attempts=Count("id"), correct=Count("id", filter=Q(is_correct=True)))
        .order_by("display_order", "slug")
    )
    return [
        {
            "subject": {"id": str(row["subject_id"]), "slug": row["slug"], "name": row["name"]},
            "accuracy": _accuracy(row["correct"], row["attempts"]),
            "attempts": row["attempts"],
        }
        for row in rows
    ]


def topic_analytics(actor) -> list[dict]:
    min_attempts, threshold = _rule()
    rows = (
        _submitted_answers(actor)
        .values(
            topic_id=F("session_item__question__topic_id"),
            slug=F("session_item__question__topic__slug"),
            name=F("session_item__question__topic__name"),
            display_order=F("session_item__question__topic__display_order"),
        )
        .annotate(attempts=Count("id"), correct=Count("id", filter=Q(is_correct=True)))
        .order_by("display_order", "slug")
    )
    result = []
    for row in rows:
        # Compare the exact ratio so rounding cannot push a failing topic over the line.
        weak = (
            row["attempts"] >= min_attempts and row["correct"] * 100 < threshold * row["attempts"]
        )
        result.append(
            {
                "topic": {"id": str(row["topic_id"]), "slug": row["slug"], "name": row["name"]},
                "accuracy": _accuracy(row["correct"], row["attempts"]),
                "attempts": row["attempts"],
                "weak_topic": weak,
                "weak_reason": (
                    f"Below {threshold:g}% accuracy over at least {min_attempts} attempts."
                    if weak
                    else None
                ),
            }
        )
    return result
