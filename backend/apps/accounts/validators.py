from __future__ import annotations

import hashlib
import urllib.error
import urllib.request

from django.conf import settings
from django.core.exceptions import ValidationError

PREFERENCE_MODES = {"untimed", "timed"}
PREFERENCE_KEYS = {"mode", "size"}


class BreachedPasswordValidator:
    """Optional HaveIBeenPwned k-anonymity check.

    Disabled by default so local development and CI never depend on the network.
    Fail-open on provider errors: availability beats an extra control at signup.
    """

    def validate(self, password: str, user=None) -> None:
        if not settings.ENABLE_BREACHED_PASSWORD_CHECK:
            return
        # SHA-1 is required by the HIBP k-anonymity protocol; it is not used for storage.
        digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()  # noqa: S324
        prefix, suffix = digest[:5], digest[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            with urllib.request.urlopen(url, timeout=3) as response:  # noqa: S310
                body = response.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError, OSError):
            return
        for line in body.splitlines():
            candidate, _, count = line.partition(":")
            if candidate == suffix and count.isdigit() and int(count) > 0:
                raise ValidationError(
                    "This password has appeared in a data breach.",
                    code="password_breached",
                )

    def get_help_text(self) -> str:
        return "Your password must not appear in known data breaches."


def validate_preference(value: object) -> dict:
    """Validate the {mode, size} study preference shape."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationError("Preference must be an object.", code="invalid")
    unknown = set(value) - PREFERENCE_KEYS
    if unknown:
        raise ValidationError("Unknown preference keys.", code="invalid")
    result: dict = {}
    if "mode" in value:
        mode = value["mode"]
        if mode not in PREFERENCE_MODES:
            raise ValidationError("Mode must be 'untimed' or 'timed'.", code="invalid")
        result["mode"] = mode
    if "size" in value:
        size = value["size"]
        if isinstance(size, bool) or not isinstance(size, int) or not 1 <= size <= 100:
            raise ValidationError("Size must be an integer from 1 to 100.", code="invalid")
        result["size"] = size
    return result
