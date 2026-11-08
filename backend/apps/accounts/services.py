from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session
from django.core import signing
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, AuthenticationFailed, NotFound, ValidationError

from apps.accounts.models import Profile, User
from apps.accounts.validators import validate_preference
from apps.core.models import AuditEvent, ExportRequest

logger = logging.getLogger(__name__)

RESET_SALT = "kabisado.password-reset"


class DuplicateEmail(APIException):
    status_code = 409
    default_detail = "Account could not be created. Check your details and try again."
    default_code = "conflict"


class InvalidCredentials(AuthenticationFailed):
    default_detail = "Invalid email or password."
    default_code = "unauthorized"


class InvalidResetToken(APIException):
    status_code = 401
    default_detail = "Link expired or already used. Request a new one."
    default_code = "unauthorized"


class StaleProfile(APIException):
    status_code = 409
    default_detail = "Profile changed in another tab. Refresh to see the latest version."
    default_code = "conflict"


class ExportAlreadyPending(APIException):
    status_code = 409
    default_detail = "Export already requested. Check back later."
    default_code = "conflict"


def _audit(actor, action: str, object_type: str = "", object_id=None, metadata=None) -> None:
    AuditEvent.objects.create(
        actor=actor,
        action=action,
        object_type=object_type,
        object_id=object_id,
        metadata=metadata or {},
    )


def _validate_password(password: str, user: User | None = None) -> None:
    try:
        validate_password(password, user)
    except DjangoValidationError as exc:
        raise ValidationError({"password": list(exc.messages)}) from exc


@transaction.atomic
def register_user(*, email: str, password: str) -> User:
    normalized = email.strip().lower()
    if User.objects.filter(email=normalized).exists():
        raise DuplicateEmail
    _validate_password(password)
    user = User.objects.create_user(email=normalized, password=password)
    _audit(user, AuditEvent.Action.REGISTER, "accounts.User", user.pk)
    return user


def start_session(request, user: User) -> None:
    """Log the user in and rotate the session key (fixation defence)."""
    login(request, user)
    request.session.cycle_key()
    request.session["last_activity"] = timezone.now().timestamp()
    user.touch_login()


def login_user(request, *, email: str, password: str) -> User:
    user = authenticate(request, username=email.strip().lower(), password=password)
    if user is None or not user.is_active:
        raise InvalidCredentials
    start_session(request, user)
    _audit(user, AuditEvent.Action.LOGIN, "accounts.User", user.pk)
    return user


def logout_user(request) -> None:
    if request.user.is_authenticated:
        _audit(request.user, AuditEvent.Action.LOGOUT, "accounts.User", request.user.pk)
    logout(request)


def make_reset_token(user: User) -> str:
    return signing.dumps(
        {"uid": str(user.pk), "token": default_token_generator.make_token(user)},
        salt=RESET_SALT,
        compress=True,
    )


def request_password_reset(*, email: str) -> None:
    """Always returns normally; unknown or inactive emails send nothing."""
    user = User.objects.filter(email=email.strip().lower(), is_active=True).first()
    if user is not None:
        _audit(user, AuditEvent.Action.PASSWORD_RESET_REQUESTED, "accounts.User", user.pk)
    if user is None:
        return
    link = f"{settings.FRONTEND_URL}/reset-password/{make_reset_token(user)}"
    try:
        send_mail(
            subject="Reset your Kabisado password",
            message=(
                "Use the link below to choose a new password. "
                "If you did not request this, you can ignore this email.\n\n"
                f"{link}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:  # noqa: BLE001 - delivery failure must not block or leak
        logger.exception("Password reset email delivery failed.")


@transaction.atomic
def confirm_password_reset(*, token: str, password: str) -> User:
    try:
        payload = signing.loads(token, salt=RESET_SALT, max_age=settings.PASSWORD_RESET_TIMEOUT)
    except (signing.BadSignature, signing.SignatureExpired) as exc:
        raise InvalidResetToken from exc

    user = User.objects.filter(pk=payload.get("uid"), is_active=True).first()
    if user is None or not default_token_generator.check_token(user, payload.get("token", "")):
        raise InvalidResetToken

    _validate_password(password, user)
    user.set_password(password)
    user.save(update_fields=["password", "updated_at"])
    invalidate_user_sessions(user)
    _audit(user, AuditEvent.Action.RESET, "accounts.User", user.pk)
    return user


def update_profile(
    user: User,
    *,
    display_name: str | None = None,
    target_exam: str | None = None,
    timezone_name: str | None = None,
    preference: dict | None = None,
    expected_updated_at: str | None = None,
) -> Profile:
    with transaction.atomic():
        profile = user.profile
        # Optimistic concurrency: the client echoes the version it loaded
        # (spec §10, concurrent profile edit).
        if (
            expected_updated_at is not None
            and profile.updated_at.isoformat() != expected_updated_at
        ):
            raise StaleProfile

        changed: list[str] = []
        user_fields: list[str] = []
        if display_name is not None:
            user.display_name = display_name.strip()
            user_fields.append("display_name")
            changed.append("display_name")
        if user_fields:
            user.save(update_fields=[*user_fields, "updated_at"])

        profile_fields: list[str] = []
        if target_exam is not None:
            profile.target_exam = target_exam
            profile_fields.append("target_exam")
            changed.append("target_exam")
        if timezone_name is not None:
            profile.timezone = timezone_name
            profile_fields.append("timezone")
            changed.append("timezone")
        if preference is not None:
            cleaned = validate_preference(preference)
            profile.study_preference = {**profile.study_preference, **cleaned}
            profile_fields.append("study_preference")
            changed.append("preference")
        if profile_fields or user_fields:
            # Bump the version on any successful edit so a stale tab is caught.
            profile.save(update_fields=[*profile_fields, "updated_at"])

        _audit(
            user,
            AuditEvent.Action.PROFILE_UPDATE,
            "accounts.Profile",
            user.pk,
            {"fields": changed},
        )
    return profile


def delete_account(request, *, user: User, password: str) -> None:
    if not user.check_password(password):
        raise ValidationError({"password": ["Incorrect password."]})
    _audit(user, AuditEvent.Action.DELETE, "accounts.User", user.pk, {"action": "account_deleted"})
    logout(request)
    user.delete()


def request_export(*, user: User) -> ExportRequest:
    export, created = ExportRequest.objects.get_or_create(
        user=user, status=ExportRequest.Status.PENDING
    )
    if not created:
        raise ExportAlreadyPending
    _audit(user, AuditEvent.Action.EXPORT, "core.ExportRequest", export.pk)
    return export


def get_export(*, user: User, export_id) -> ExportRequest:
    export = ExportRequest.objects.filter(pk=export_id, user=user).first()
    if export is None:
        raise NotFound("Not found.")
    return export


def invalidate_user_sessions(user: User) -> int:
    """Delete every session belonging to the user.

    shortcut: scans the session table; replace with a session-version column if
    the table grows large or sessions move to a shared store.
    """
    removed = 0
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    for session in sessions.iterator():
        data = session.get_decoded()
        if data.get("_auth_user_id") == str(user.pk):
            session.delete()
            removed += 1
    return removed
