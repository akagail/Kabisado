from __future__ import annotations

from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts import services
from apps.accounts.serializers import (
    CsrfSerializer,
    DeleteAccountSerializer,
    ExportRequestSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileEnvelopeSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    SessionSerializer,
    profile_payload,
    session_payload,
)
from apps.accounts.throttles import (
    LoginEmailThrottle,
    LoginIpThrottle,
    RegisterIpThrottle,
    ResetConfirmIpThrottle,
    ResetEmailThrottle,
    ResetIpThrottle,
)


def _private(response: Response) -> Response:
    response["Cache-Control"] = "private, no-store"
    return response


class CsrfView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    @extend_schema(responses={200: CsrfSerializer})
    def get(self, request):
        """Deliver the token in the body so the cookie can stay HttpOnly."""
        return Response({"csrfToken": get_token(request._request)})


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterIpThrottle]

    @extend_schema(request=RegisterSerializer, responses={201: SessionSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.register_user(**serializer.validated_data)
        services.start_session(request, user)
        return _private(Response(session_payload(user), status=status.HTTP_201_CREATED))


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginIpThrottle, LoginEmailThrottle]

    @extend_schema(request=LoginSerializer, responses={200: SessionSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.login_user(request, **serializer.validated_data)
        return _private(Response(session_payload(user)))


class LogoutView(APIView):
    # Idempotent: repeated logouts (same CSRF token, second request after the
    # first already flushed the session) all return 204 per spec §10.
    permission_classes = [AllowAny]

    @extend_schema(request=None, responses={204: None})
    def post(self, request):
        services.logout_user(request)
        return _private(Response(status=status.HTTP_204_NO_CONTENT))


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ResetIpThrottle, ResetEmailThrottle]

    @extend_schema(request=PasswordResetRequestSerializer, responses={202: None})
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.request_password_reset(**serializer.validated_data)
        return _private(
            Response(
                {"message": "If that address exists, a reset link has been sent."},
                status=status.HTTP_202_ACCEPTED,
            )
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ResetConfirmIpThrottle]

    @extend_schema(request=PasswordResetConfirmSerializer, responses={200: SessionSerializer})
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.confirm_password_reset(**serializer.validated_data)
        services.start_session(request, user)
        return _private(Response(session_payload(user)))


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: SessionSerializer})
    def get(self, request):
        return _private(Response(session_payload(request.user)))

    @extend_schema(request=ProfileUpdateSerializer, responses={200: ProfileEnvelopeSerializer})
    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        profile = services.update_profile(
            request.user,
            display_name=data.get("display_name"),
            target_exam=data.get("target_exam"),
            timezone_name=data.get("timezone"),
            preference=data.get("preference"),
        )
        return _private(Response({"profile": profile_payload(profile)}))

    @extend_schema(request=DeleteAccountSerializer, responses={204: None})
    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.delete_account(
            request, user=request.user, password=serializer.validated_data["password"]
        )
        return _private(Response(status=status.HTTP_204_NO_CONTENT))


class ExportRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={201: ExportRequestSerializer})
    def post(self, request):
        export = services.request_export(user=request.user)
        return _private(Response(ExportRequestSerializer(export).data, status=201))


class ExportRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: ExportRequestSerializer})
    def get(self, request, export_id):
        export = services.get_export(user=request.user, export_id=export_id)
        return _private(Response(ExportRequestSerializer(export).data))
