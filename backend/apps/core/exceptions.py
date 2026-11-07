from __future__ import annotations

from typing import Any

from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Any:
    """Wrap DRF errors in the stable Kabisado error envelope."""
    response = exception_handler(exc, context)
    if response is None:
        return None

    code = getattr(exc, "default_code", "error")
    message = "Request could not be processed."
    fields = None

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

    response.data = {
        "error": {
            "code": code,
            "message": message,
            "fields": fields,
        }
    }
    return response
