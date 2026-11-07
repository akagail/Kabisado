from __future__ import annotations

from apps.accounts.models import User
from apps.core.models import ExportRequest


def get_user_by_email(email: str) -> User | None:
    return User.objects.filter(email=email.strip().lower(), is_active=True).first()


def get_export_for_user(user: User, export_id) -> ExportRequest | None:
    return ExportRequest.objects.filter(pk=export_id, user=user).first()
