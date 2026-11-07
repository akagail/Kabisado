from __future__ import annotations

from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException, PermissionDenied


class CsrfError(APIException):
    status_code = 403
    default_detail = "Session expired. Please try again."
    default_code = "csrf_error"


class CsrfEnforcingSessionAuthentication(SessionAuthentication):
    """Session auth that also enforces CSRF for anonymous unsafe requests.

    DRF marks every APIView csrf_exempt and its default SessionAuthentication
    only checks CSRF once a user is authenticated. Public state-changing
    endpoints (register/login/reset) still need the check (ADR-0004).
    """

    def authenticate_header(self, request) -> str:
        # Makes DRF return 401 (not 403) when the session is missing.
        return "Session"

    def _enforce(self, request) -> None:
        try:
            self.enforce_csrf(request)
        except PermissionDenied as exc:
            raise CsrfError from exc

    def authenticate(self, request):
        user = getattr(request._request, "user", None)
        if user is None or not user.is_authenticated:
            self._enforce(request)
            return None
        self._enforce(request)
        return user, None
