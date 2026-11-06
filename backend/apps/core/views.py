from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def liveness(request):
    """Process is running."""
    return JsonResponse({"status": "ok"})


@require_GET
def readiness(request):
    """Database is reachable."""
    try:
        connection.ensure_connection()
    except Exception:  # noqa: BLE001 - any connection failure means not ready
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})
