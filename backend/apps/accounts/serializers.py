from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.accounts.models import TARGET_EXAM_CHOICES, Profile, User
from apps.accounts.validators import validate_preference
from apps.core.models import ExportRequest


def user_payload(user: User) -> dict:
    return {"id": str(user.pk), "email": user.email}


def profile_payload(profile: Profile) -> dict:
    return {
        "id": str(profile.user_id),
        "display_name": profile.user.display_name,
        "target_exam": profile.target_exam or None,
        "timezone": profile.timezone,
        "preference": profile.study_preference,
        "updated_at": profile.updated_at.isoformat(),
    }


def session_payload(user: User) -> dict:
    profile = user.profile
    return {"user": user_payload(user), "profile": profile_payload(profile)}


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class ProfileSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    display_name = serializers.CharField()
    target_exam = serializers.CharField(allow_null=True)
    timezone = serializers.CharField()
    preference = serializers.JSONField()


class SessionSerializer(serializers.Serializer):
    user = UserSerializer()
    profile = ProfileSerializer()


class ProfileEnvelopeSerializer(serializers.Serializer):
    profile = ProfileSerializer()


class CsrfSerializer(serializers.Serializer):
    csrfToken = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class ProfileUpdateSerializer(serializers.Serializer):
    display_name = serializers.CharField(max_length=80, required=False, allow_blank=True)
    target_exam = serializers.ChoiceField(
        choices=[value for value, _ in TARGET_EXAM_CHOICES],
        required=False,
        allow_blank=True,
    )
    timezone = serializers.CharField(max_length=64, required=False)
    preference = serializers.JSONField(required=False)
    # Opaque version echoed from GET /me/; compared as a string so timezone
    # rendering cannot make an unchanged profile look stale.
    updated_at = serializers.CharField(required=False)

    def validate_preference(self, value):
        try:
            return validate_preference(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class ExportRequestSerializer(serializers.ModelSerializer):
    export_id = serializers.UUIDField(source="id", read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ExportRequest
        fields = ["export_id", "status", "requested_at", "completed_at", "download_url"]

    def get_download_url(self, obj: ExportRequest) -> str | None:
        return None
