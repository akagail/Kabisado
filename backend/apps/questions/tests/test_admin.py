from __future__ import annotations

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_staff_can_open_question_bank_admin_pages(admin_client, settings):
    # The test run has no collectstatic manifest; plain storage renders the pages.
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

    for name in (
        "questions_question_changelist",
        "questions_contentflag_changelist",
    ):
        assert admin_client.get(reverse(f"admin:{name}")).status_code == 200


def test_anonymous_user_cannot_open_question_bank_admin(client):
    response = client.get(reverse("admin:questions_question_changelist"))

    assert response.status_code == 302
    assert "/admin/login/" in response["Location"]
