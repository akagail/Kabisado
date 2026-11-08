from __future__ import annotations

import pytest
from django.conf import settings
from django.core import mail
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.core.models import AuditEvent

pytestmark = pytest.mark.django_db

VALID_PASSWORD = "CorrectHorse123!"

REGISTER = "/api/v1/auth/register/"
LOGIN = "/api/v1/auth/login/"
LOGOUT = "/api/v1/auth/logout/"
RESET = "/api/v1/auth/password-reset/"
RESET_CONFIRM = "/api/v1/auth/password-reset/confirm/"
ME = "/api/v1/me/"


def test_register_creates_profile_case_insensitive_email_and_session(api, csrf):
    token = csrf()
    response = api.post(
        REGISTER,
        {"email": "Learner@Example.COM", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=token,
    )

    assert response.status_code == 201
    assert response.json()["user"]["email"] == "learner@example.com"
    assert response.json()["profile"]["display_name"] == ""
    user = User.objects.get(email="learner@example.com")
    assert user.profile is not None

    cookie = response.cookies[settings.SESSION_COOKIE_NAME]
    assert cookie["httponly"]
    assert cookie["samesite"] == "Lax"

    assert api.get(ME).status_code == 200


def test_register_rejects_duplicate_email_with_generic_409(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    response = api.post(
        REGISTER,
        {"email": "LEARNER@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "conflict"
    assert "learner@example.com" not in response.json()["error"]["message"].lower()


def test_register_rejects_short_password(api, csrf):
    response = api.post(
        REGISTER,
        {"email": "learner@example.com", "password": "short"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert "password" in response.json()["error"]["fields"]


def test_login_success_and_logout_invalidates_session(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    api.post(LOGOUT, HTTP_X_CSRFTOKEN=csrf())
    assert api.get(ME).status_code == 401

    login = api.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert login.status_code == 200
    assert api.get(ME).status_code == 200

    logout = api.post(LOGOUT, HTTP_X_CSRFTOKEN=csrf())
    assert logout.status_code == 204
    assert api.get(ME).status_code == 401


def test_login_invalid_credentials_are_generic(api, csrf):
    response = api.post(
        LOGIN,
        {"email": "nobody@example.com", "password": "WrongPassword123!"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password."


def test_inactive_account_login_is_generic(api, csrf):
    User.objects.create_user(email="inactive@example.com", password=VALID_PASSWORD, is_active=False)

    response = api.post(
        LOGIN,
        {"email": "inactive@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password."


def test_csrf_is_required_for_anonymous_post(api):
    response = api.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "csrf_error"


def test_login_is_rate_limited_with_retry_after(api, csrf):
    payload = {"email": "learner@example.com", "password": "WrongPassword123!"}
    responses = [api.post(LOGIN, payload, format="json", HTTP_X_CSRFTOKEN=csrf()) for _ in range(6)]

    assert responses[-1].status_code == 429
    assert responses[-1]["Retry-After"]
    assert responses[-1].json()["error"]["code"] == "rate_limited"


def test_password_reset_is_generic_for_unknown_email(api, csrf):
    response = api.post(
        RESET,
        {"email": "nobody@example.com"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 202
    assert len(mail.outbox) == 0


def test_password_reset_confirm_sets_password_and_invalidates_sessions(api, csrf):
    User.objects.create_user(email="learner@example.com", password=VALID_PASSWORD)

    other = APIClient(enforce_csrf_checks=True)
    other_token = other.get("/api/v1/auth/csrf/").json()["csrfToken"]
    other.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=other_token,
    )
    assert other.get(ME).status_code == 200

    reset = api.post(
        RESET,
        {"email": "learner@example.com"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert reset.status_code == 202
    assert len(mail.outbox) == 1
    token = mail.outbox[0].body.split("/reset-password/")[1].strip()

    confirm = api.post(
        RESET_CONFIRM,
        {"token": token, "password": "BrandNewPassword456!"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert confirm.status_code == 200
    assert other.get(ME).status_code == 401

    old_login = api.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert old_login.status_code == 401


def test_password_reset_request_audits_event(api, csrf, mailoutbox):
    User.objects.create_user(email="learner@example.com", password=VALID_PASSWORD)
    api.post(RESET, {"email": "learner@example.com"}, format="json", HTTP_X_CSRFTOKEN=csrf())

    assert len(mailoutbox) == 1

    actions = list(AuditEvent.objects.values_list("action", flat=True))
    assert AuditEvent.Action.PASSWORD_RESET_REQUESTED in actions
    assert not any("learner@example.com" in str(e) for e in AuditEvent.objects.all())


def test_logout_is_idempotent(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    first = api.post(LOGOUT, HTTP_X_CSRFTOKEN=csrf())
    assert first.status_code == 204
    second = api.post(LOGOUT, HTTP_X_CSRFTOKEN=csrf())
    assert second.status_code == 204
    assert api.get(ME).status_code == 401


def test_server_error_envelope_uses_server_error():
    """Generic 500 responses map to the spec's server_error code."""
    from rest_framework.exceptions import APIException

    from apps.core import exceptions as exc_mod

    class FakeServerError(APIException):
        status_code = 500
        default_code = "error"

    resp = exc_mod.api_exception_handler(
        FakeServerError(),
        {"view": None, "args": (), "kwargs": {}},
    )
    assert resp is not None
    assert resp.status_code == 500
    assert resp.data["error"]["code"] == "server_error"
    assert resp.data["error"]["message"] == "Something went wrong. Please try again."


def test_password_reset_token_is_single_use(api, csrf):
    User.objects.create_user(email="learner@example.com", password=VALID_PASSWORD)
    api.post(
        RESET,
        {"email": "learner@example.com"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    token = mail.outbox[0].body.split("/reset-password/")[1].strip()

    first = api.post(
        RESET_CONFIRM,
        {"token": token, "password": "BrandNewPassword456!"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    second = api.post(
        RESET_CONFIRM,
        {"token": token, "password": "AnotherPassword789!"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert first.status_code == 200
    assert second.status_code == 401
    assert second.json()["error"]["code"] == "unauthorized"
