from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import BaseModel


class Question(BaseModel):
    """A multiple-choice item. Lifecycle and publish rules live in services."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_REVIEW = "in_review", "In review"
        PUBLISHED = "published", "Published"
        RETIRED = "retired", "Retired"

    class Origin(models.TextChoices):
        HUMAN = "human", "Human"
        AI_ASSISTED = "ai_assisted", "AI-assisted"
        AI_GENERATED = "ai_generated", "AI-generated"

    topic = models.ForeignKey("catalog.Topic", on_delete=models.PROTECT, related_name="questions")
    stem = models.TextField()
    # SHA-256 of the whitespace-collapsed, lower-cased stem (duplicate detection).
    stem_hash = models.CharField(max_length=64, db_index=True)
    explanation = models.TextField(blank=True, default="")
    provenance = models.TextField(blank=True, default="")
    difficulty = models.PositiveSmallIntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    origin = models.CharField(max_length=16, choices=Origin.choices, default=Origin.HUMAN)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_questions",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_questions",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["topic", "status"], name="questions_topic_status_idx"),
            models.Index(fields=["status", "difficulty"], name="questions_status_diff_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(difficulty__gte=1, difficulty__lte=5),
                name="questions_difficulty_1_5",
            )
        ]

    def __str__(self) -> str:
        return self.stem[:80]


class Choice(BaseModel):
    """One answer option. The partial unique index allows at most one correct."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    rationale = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "display_order"],
                name="questions_choice_unique_order",
            ),
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_correct=True),
                name="questions_choice_one_correct",
            ),
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ContentFlag(BaseModel):
    class Reason(models.TextChoices):
        INCORRECT_ANSWER = "incorrect_answer", "Incorrect answer"
        UNCLEAR = "unclear", "Unclear wording"
        TYPO = "typo", "Typo"
        COPYRIGHT = "copyright", "Copyright or provenance"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        RESOLVED = "resolved", "Resolved"
        DISMISSED = "dismissed", "Dismissed"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="flags")
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="content_flags",
    )
    reason = models.CharField(max_length=32, choices=Reason.choices)
    note = models.TextField(blank=True, default="")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="resolved_content_flags",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "created_at"], name="questions_flag_status_idx")]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "reporter"],
                condition=models.Q(status="open"),
                name="questions_flag_one_open_per_reporter",
            )
        ]

    def __str__(self) -> str:
        return f"{self.reason} on {self.question_id} ({self.status})"
