from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """Base for domain models: UUID primary key and audit timestamps."""

    class Meta:
        abstract = True


class AuditEvent(UUIDModel):
    """Append-only record of security-relevant actions. No PII in metadata."""

    class Action(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        REGISTER = "register", "Register"
        RESET = "reset", "Password reset"
        PROFILE_UPDATE = "profile_update", "Profile update"
        DELETE = "delete", "Account deletion"
        EXPORT = "export", "Export request"

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_events",
    )
    action = models.CharField(max_length=32, choices=Action.choices)
    object_type = models.CharField(max_length=64, blank=True, default="")
    object_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["actor", "created_at"])]

    def __str__(self) -> str:
        return f"{self.action} at {self.created_at:%Y-%m-%d %H:%M}"


class ExportRequest(UUIDModel):
    """User data-portability request. Fulfilled manually at alpha."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        READY = "ready", "Ready"
        EXPIRED = "expired", "Expired"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="export_requests",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    file_path = models.TextField(null=True, blank=True)  # noqa: DJ001 - nullable per DB design

    class Meta:
        ordering = ["-requested_at"]
        indexes = [models.Index(fields=["user", "-requested_at"])]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(status="pending"),
                name="core_export_request_one_pending_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"Export {self.pk} ({self.status})"
