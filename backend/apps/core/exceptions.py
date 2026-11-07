from __future__ import annotations

from typing import Any

from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Any:
    """Wrap DRF errors in the stable Kabisado error envelope."""
    response = exception_handler(exc, context)
    if response is None:
        return None

    message = ""
    fields = None
    code = getattr(exc, "default_code", "error")
    status_code = response.status_code

    # Map specific codes first; the 500 fallback must override any detail text so
    # it never leaks internals.
    if status_code == 400:
        code = "validation_error"
    elif status_code == 401:
        code = "unauthorized"
    elif status_code == 403 and code != "csrf_error":
        code = "forbidden"
    elif status_code == 404:
        code = "not_found"
    elif status_code == 409:
        code = "conflict"
    elif status_code == 429:
        code = "rate_limited"

    detail = response.data
    if isinstance(detail, dict):
        if "detail" in detail:
            message = str(detail["detail"])
        else:
            fields = detail
            message = "Validation failed."
    elif isinstance(detail, list):
        fields = {"non_field_errors": detail}
        message = "Validation failed."
    else:
        message = str(detail)
        fields = None

    if status_code == 500:
        # DRF 500s must never expose internals; use a stable generic message.
        message = "Something went wrong. Please try again."
        fields = None
        code = "server_error"

    response.data = {
        "error": {
            "code": code,
            "message": message,
            "fields": fields,
        }
    }
    return response
