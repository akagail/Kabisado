from __future__ import annotations

from rest_framework.throttling import SimpleRateThrottle


class _IpScopedThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class _EmailScopedThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        data = getattr(request, "data", {}) or {}
        email = str(data.get("email", "")).strip().lower() if isinstance(data, dict) else ""
        if not email:
            return None
        return self.cache_format % {"scope": self.scope, "ident": email}


class LoginIpThrottle(_IpScopedThrottle):
    scope = "login_ip"


class LoginEmailThrottle(_EmailScopedThrottle):
    scope = "login_email"


class RegisterIpThrottle(_IpScopedThrottle):
    scope = "register_ip"


class ResetIpThrottle(_IpScopedThrottle):
    scope = "reset_ip"


class ResetEmailThrottle(_EmailScopedThrottle):
    scope = "reset_email"


class ResetConfirmIpThrottle(_IpScopedThrottle):
    scope = "reset_confirm_ip"
