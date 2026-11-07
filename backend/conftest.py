from __future__ import annotations

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

VALID_PASSWORD = "CorrectHorse123!"  # noqa: S105 - test-only value


@pytest.fixture(autouse=True)
def clear_rate_limit_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture(autouse=True)
def locmem_email(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def api():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def csrf(api):
    def _token() -> str:
        return api.get("/api/v1/auth/csrf/").json()["csrfToken"]

    return _token
