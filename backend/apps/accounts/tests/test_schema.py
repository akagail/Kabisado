from __future__ import annotations

from drf_spectacular.generators import SchemaGenerator


def test_openapi_schema_covers_auth_and_me():
    schema = SchemaGenerator().get_schema(request=None, public=True)

    for path in (
        "/api/v1/auth/register/",
        "/api/v1/auth/login/",
        "/api/v1/auth/logout/",
        "/api/v1/auth/csrf/",
        "/api/v1/me/",
        "/api/v1/me/export/",
    ):
        assert path in schema["paths"]
