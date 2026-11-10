from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("The email address is required.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Profile.objects.get_or_create(user=user)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_staff and is_superuser set.")
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username: str):
        return self.get(email=username.lower())


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Email-identified account. Email is normalized to lower case in the manager."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=80, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email

    def touch_login(self) -> None:
        self.last_login_at = timezone.now()
        self.save(update_fields=["last_login_at", "updated_at"])


class Profile(TimeStampedModel):
    """Profile preferences. `display_name` lives on User (approved DB design)."""

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    target_exam = models.ForeignKey(
        "catalog.Exam",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="targeted_by_profiles",
    )
    timezone = models.CharField(max_length=64, default="Asia/Manila")
    study_preference = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Profile for {self.user_id}"
