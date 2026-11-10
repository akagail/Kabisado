from __future__ import annotations

import pytest
from django.core.management import call_command
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_staff_can_open_every_catalogue_admin_page(admin_client, settings):
    # The test run has no collectstatic manifest; plain storage renders the pages.
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    call_command("seed_cse_catalogue", force=True)

    for name in (
        "catalog_examfamily_changelist",
        "catalog_exam_changelist",
        "catalog_examversion_changelist",
        "catalog_subject_changelist",
        "catalog_topic_changelist",
    ):
        assert admin_client.get(reverse(f"admin:{name}")).status_code == 200


def test_anonymous_user_cannot_open_catalogue_admin(client):
    response = client.get(reverse("admin:catalog_exam_changelist"))

    assert response.status_code == 302
    assert "/admin/login/" in response["Location"]
