from __future__ import annotations

import hashlib
import urllib.error

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.validators import BreachedPasswordValidator, validate_preference


class _FakeResponse:
    def __init__(self, body: str):
        self.body = body

    def read(self) -> bytes:
        return self.body.encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_breached_validator_is_off_by_default(settings, monkeypatch):
    settings.ENABLE_BREACHED_PASSWORD_CHECK = False
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: _FakeResponse(""))

    BreachedPasswordValidator().validate("CorrectHorse123!")


def test_breached_validator_rejects_a_known_suffix(settings, monkeypatch):
    settings.ENABLE_BREACHED_PASSWORD_CHECK = True
    password = "CorrectHorse123!"
    digest = hashlib.sha1(password.encode()).hexdigest().upper()  # noqa: S324
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *a, **k: _FakeResponse(f"{digest[5:]}:42"),
    )

    with pytest.raises(ValidationError):
        BreachedPasswordValidator().validate(password)


def test_breached_validator_fails_open_when_the_service_is_down(settings, monkeypatch):
    settings.ENABLE_BREACHED_PASSWORD_CHECK = True

    def _raise(*args, **kwargs):
        raise urllib.error.URLError("down")

    monkeypatch.setattr("urllib.request.urlopen", _raise)

    BreachedPasswordValidator().validate("CorrectHorse123!")


def test_preference_shape_is_validated():
    assert validate_preference({"mode": "timed", "size": 20}) == {"mode": "timed", "size": 20}
    with pytest.raises(ValidationError):
        validate_preference({"mode": "wild"})
    with pytest.raises(ValidationError):
        validate_preference({"size": 0})
    with pytest.raises(ValidationError):
        validate_preference({"extra": True})
