from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel


class ExamFamily(BaseModel):
    """Top-level grouping, e.g. `cse` for the Philippine Civil Service Examination."""

    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["slug"]
        verbose_name_plural = "exam families"

    def __str__(self) -> str:
        return self.name


class Exam(BaseModel):
    class Level(models.TextChoices):
        PROFESSIONAL = "professional", "Professional"
        SUBPROFESSIONAL = "subprofessional", "Subprofessional"

    family = models.ForeignKey(ExamFamily, on_delete=models.PROTECT, related_name="exams")
    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=120)
    level = models.CharField(max_length=32, choices=Level.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["slug"]
        constraints = [
            models.UniqueConstraint(
                fields=["family", "slug"], name="catalog_exam_unique_slug_per_family"
            )
        ]

    def __str__(self) -> str:
        return self.name


class ExamVersion(BaseModel):
    """One published bulletin. Subject/topic trees are scoped to a version (ADR-0008)."""

    exam = models.ForeignKey(Exam, on_delete=models.PROTECT, related_name="versions")
    slug = models.SlugField(max_length=64)
    label = models.CharField(max_length=160)
    source_url = models.URLField(max_length=500)
    published_at = models.DateField()
    accessed_at = models.DateField(null=True, blank=True)
    # Left null until an official CSC issuance states the figure (cse-exam-reference §5).
    item_count = models.PositiveIntegerField(null=True, blank=True)
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    passing_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at", "slug"]
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "slug"], name="catalog_exam_version_unique_slug_per_exam"
            )
        ]

    def __str__(self) -> str:
        return f"{self.exam} — {self.label}"


class Subject(BaseModel):
    exam_version = models.ForeignKey(ExamVersion, on_delete=models.PROTECT, related_name="subjects")
    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=120)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "slug"]
        constraints = [
            models.UniqueConstraint(
                fields=["exam_version", "slug"], name="catalog_subject_unique_slug_per_version"
            )
        ]

    def __str__(self) -> str:
        return self.name


class Topic(BaseModel):
    """Official coverage area. Immutable once seeded; practice items reference it."""

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="topics")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
    )
    slug = models.SlugField(max_length=64)
    name = models.CharField(max_length=120)
    display_order = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["display_order", "slug"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "parent", "slug"],
                name="catalog_topic_unique_slug_per_parent",
            ),
            # NULL parents are distinct in PostgreSQL, so root topics need their own rule.
            models.UniqueConstraint(
                fields=["subject", "slug"],
                condition=models.Q(parent__isnull=True),
                name="catalog_topic_unique_root_slug",
            ),
        ]

    def __str__(self) -> str:
        return self.name
