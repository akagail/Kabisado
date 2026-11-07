from __future__ import annotations

import time

from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone


class SessionInactivityMiddleware:
    """Enforce the 30-minute sliding inactivity timeout (ADR-0004)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/") and request.session.get("_auth_user_id"):
            last = request.session.get("last_activity")
            now = time.time()
            if last is not None and now - float(last) > settings.SESSION_INACTIVITY_SECONDS:
                logout(request)
                return JsonResponse(
                    {
                        "error": {
                            "code": "unauthorized",
                            "message": "Please sign in to continue.",
                            "fields": None,
                        }
                    },
                    status=401,
                )
            request.session["last_activity"] = timezone.now().timestamp()
        return self.get_response(request)
