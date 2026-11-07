from __future__ import annotations

from django.urls import path

from apps.accounts.views import (
    CsrfView,
    ExportRequestCreateView,
    ExportRequestDetailView,
    LoginView,
    LogoutView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path(
        "auth/password-reset/",
        PasswordResetRequestView.as_view(),
        name="auth-password-reset",
    ),
    path(
        "auth/password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
    path("auth/csrf/", CsrfView.as_view(), name="auth-csrf"),
    path("me/", MeView.as_view(), name="me"),
    path("me/export/", ExportRequestCreateView.as_view(), name="me-export"),
    path(
        "me/export/<uuid:export_id>/",
        ExportRequestDetailView.as_view(),
        name="me-export-detail",
    ),
]
