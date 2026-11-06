import pytest
from django.test import Client


@pytest.mark.django_db
def test_liveness_returns_ok():
    response = Client().get("/health/live/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_readiness_returns_ok_when_database_is_reachable():
    response = Client().get("/health/ready/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
