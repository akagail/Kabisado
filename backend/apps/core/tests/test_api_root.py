import pytest
from django.test import Client


@pytest.mark.django_db
def test_api_root_returns_version():
    response = Client().get("/api/v1/")

    assert response.status_code == 200
    assert response.json() == {"name": "Kabisado API", "version": "v1"}
