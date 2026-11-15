from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel


class PracticeSession(BaseModel):
    """A single practice session: untimed or timed."""

    class Mode(models.TextChoices):
        UNTIMED = "untimed", "Untimed"
        TIMED = "timed", "Timed"

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"
        SUBMITTED = "submitted", "Submitted"
        EXPIRED = "expired", "Expired"
        ABANDONED = "abandoned", "Abandoned"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="practice_sessions"
    )
    exam_version = models.ForeignKey(
        "catalog.ExamVersion", on_delete=models.PROTECT, related_name="practice_sessions"
    )
    mode = models.CharField(max_length=16, choices=Mode.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.IN_PROGRESS)
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score_correct = models.PositiveSmallIntegerField(null=True, blank=True)
    score_total = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "-started_at"]),
            models.Index(fields=["status", "expires_at"]),
        ]

    def __str__(self) -> str:
        return f"Practice session {self.id} ({self.status})"

    def save(self, *args, **kwargs):
        if self.mode == self.Mode.TIMED and not self.time_limit_seconds:
            raise ValidationError("Time limit must be set for timed sessions.")
        super().save(*args, **kwargs)


class SessionItem(BaseModel):
    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE, related_name="items")
    question = models.ForeignKey(
        "questions.Question", on_delete=models.PROTECT, related_name="session_items"
    )
    display_order = models.PositiveSmallIntegerField()
    snapshot_stem = models.TextField()
    snapshot_options = models.JSONField()  # [{id, text, is_correct}]
    snapshot_explanation = models.TextField()
    snapshot_provenance = models.TextField()
    snapshot_difficulty = models.SmallIntegerField()

    class Meta:
        unique_together = (("session", "display_order"), ("session", "question"))
        ordering = ["display_order"]

    def __str__(self) -> str:
        return f"Session item {self.session_id} position {self.display_order}"


class AttemptAnswer(BaseModel):
    session_item = models.ForeignKey(SessionItem, on_delete=models.CASCADE, related_name="answers")
    selected_choice = models.ForeignKey(
        "questions.Choice", on_delete=models.PROTECT, null=True, blank=True
    )
    is_correct = models.BooleanField(null=True)
    answered_at = models.DateTimeField(auto_now=True)
    time_spent_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("session_item",)

    def __str__(self) -> str:
        return f"Answer for item {self.session_item_id}"
