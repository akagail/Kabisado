from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.core.models import ExportRequest

pytestmark = pytest.mark.django_db

VALID_PASSWORD = "CorrectHorse123!"
REGISTER = "/api/v1/auth/register/"
ME = "/api/v1/me/"
EXPORT = "/api/v1/me/export/"


def _logged_in(api, csrf, email="learner@example.com"):
    api.post(
        REGISTER,
        {"email": email, "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )


def test_me_requires_authentication(api):
    response = api.get(ME)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_profile_can_be_read_and_updated(api, csrf):
    _logged_in(api, csrf, "ada@example.com")

    patch = api.patch(
        ME,
        {
            "display_name": "Ada",
            "target_exam": "professional",
            "timezone": "Asia/Manila",
            "preference": {"mode": "timed", "size": 20},
        },
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert patch.status_code == 200
    profile = patch.json()["profile"]
    assert profile["display_name"] == "Ada"
    assert profile["target_exam"] == "professional"
    assert profile["preference"] == {"mode": "timed", "size": 20}

    read = api.get(ME).json()
    assert read["user"]["email"] == "ada@example.com"
    assert read["profile"]["display_name"] == "Ada"


def test_profile_rejects_invalid_preference(api, csrf):
    _logged_in(api, csrf)

    response = api.patch(
        ME,
        {"preference": {"mode": "wild", "size": 999}},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert response.status_code == 400
    assert "preference" in response.json()["error"]["fields"]


def test_stale_profile_update_is_rejected(api, csrf):
    _logged_in(api, csrf)
    version = api.get(ME).json()["profile"]["updated_at"]

    first = api.patch(
        ME,
        {"display_name": "First", "updated_at": version},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert first.status_code == 200

    # The second tab still holds the old version.
    stale = api.patch(
        ME,
        {"display_name": "Second", "updated_at": version},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "conflict"
    assert User.objects.get(email="learner@example.com").display_name == "First"


def test_export_request_and_status(api, csrf):
    _logged_in(api, csrf)

    created = api.post(EXPORT, format="json", HTTP_X_CSRFTOKEN=csrf())
    assert created.status_code == 201
    export_id = created.json()["export_id"]
    assert created.json()["status"] == "pending"

    detail = api.get(f"{EXPORT}{export_id}/")
    assert detail.status_code == 200
    assert detail.json()["download_url"] is None


def test_second_pending_export_returns_409(api, csrf):
    _logged_in(api, csrf)

    api.post(EXPORT, format="json", HTTP_X_CSRFTOKEN=csrf())
    second = api.post(EXPORT, format="json", HTTP_X_CSRFTOKEN=csrf())

    assert second.status_code == 409
    assert second.json()["error"]["code"] == "conflict"


def test_export_of_another_user_is_not_found(api, csrf):
    _logged_in(api, csrf, "owner@example.com")
    export_id = api.post(EXPORT, format="json", HTTP_X_CSRFTOKEN=csrf()).json()["export_id"]

    intruder = APIClient(enforce_csrf_checks=True)
    token = intruder.get("/api/v1/auth/csrf/").json()["csrfToken"]
    intruder.post(
        REGISTER,
        {"email": "intruder@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=token,
    )

    response = intruder.get(f"{EXPORT}{export_id}/")

    assert response.status_code == 404
    assert ExportRequest.objects.filter(pk=export_id).exists()


def test_delete_account_requires_password_then_removes_user(api, csrf):
    _logged_in(api, csrf)
    user_id = User.objects.get(email="learner@example.com").pk

    wrong = api.delete(
        ME,
        {"password": "WrongPassword123!"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    assert wrong.status_code == 400
    assert "password" in wrong.json()["error"]["fields"]
    assert User.objects.filter(pk=user_id).exists()

    deleted = api.delete(
        ME,
        {"password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert deleted.status_code == 204
    assert not User.objects.filter(pk=user_id).exists()
    assert api.get(ME).status_code == 401
