from rest_framework.exceptions import ValidationError

from apps.core.exceptions import api_exception_handler


def test_validation_error_uses_error_envelope():
    response = api_exception_handler(
        ValidationError({"email": ["Enter a valid email address."]}),
        {},
    )

    assert response is not None
    assert response.status_code == 400
    assert response.data == {
        "error": {
            "code": "validation_error",
            "message": "Validation failed.",
            "fields": {"email": ["Enter a valid email address."]},
        }
    }
