from __future__ import annotations

from django.http import JsonResponse


def csrf_failure(request, reason: str = "") -> JsonResponse:
    """Stable JSON envelope for Django's CSRF failures (ADR-0004)."""
    return JsonResponse(
        {
            "error": {
                "code": "csrf_error",
                "message": "Session expired. Please try again.",
                "fields": None,
            }
        },
        status=403,
    )
