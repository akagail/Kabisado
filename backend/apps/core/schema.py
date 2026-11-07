from __future__ import annotations

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CsrfSessionAuthExtension(OpenApiAuthenticationExtension):
    target_class = "apps.core.authentication.CsrfEnforcingSessionAuthentication"
    name = "sessionAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": settings.SESSION_COOKIE_NAME,
        }
