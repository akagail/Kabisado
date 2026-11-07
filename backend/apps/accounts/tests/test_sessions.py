from __future__ import annotations

import time

import pytest
from django.contrib.sessions.models import Session

from apps.accounts.models import User
from apps.core.models import AuditEvent

pytestmark = pytest.mark.django_db

VALID_PASSWORD = "CorrectHorse123!"
REGISTER = "/api/v1/auth/register/"
LOGIN = "/api/v1/auth/login/"
ME = "/api/v1/me/"


def test_session_inactivity_expires_the_session(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    session = api.session
    session["last_activity"] = time.time() - 31 * 60
    session.save()

    response = api.get(ME)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"
    assert not Session.objects.filter(session_key=session.session_key).exists()


def test_session_activity_is_refreshed_within_timeout(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    session = api.session
    session["last_activity"] = time.time() - 5 * 60
    session.save()

    assert api.get(ME).status_code == 200


def test_login_rotates_the_session_key(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    first_key = api.session.session_key

    api.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    assert api.session.session_key != first_key


def test_register_and_login_are_audited_without_pii(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )
    api.post(
        LOGIN,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    actions = list(AuditEvent.objects.values_list("action", flat=True))

    assert AuditEvent.Action.REGISTER in actions
    assert AuditEvent.Action.LOGIN in actions
    assert not any("learner@example.com" in str(event) for event in AuditEvent.objects.all())


def test_email_is_never_stored_in_audit_metadata(api, csrf):
    api.post(
        REGISTER,
        {"email": "learner@example.com", "password": VALID_PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf(),
    )

    for event in AuditEvent.objects.all():
        assert "learner@example.com" not in str(event.metadata)
    assert User.objects.get(email="learner@example.com").profile is not None
