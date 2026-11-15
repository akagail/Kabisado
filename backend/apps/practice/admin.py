from django.contrib import admin

from apps.practice.models import AttemptAnswer, PracticeSession, SessionItem


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mode", "status", "started_at", "submitted_at")
    list_filter = ("mode", "status")
    search_fields = ("user__email",)
    readonly_fields = (
        "id",
        "user",
        "exam_version",
        "mode",
        "status",
        "time_limit_seconds",
        "started_at",
        "expires_at",
        "submitted_at",
        "score_correct",
        "score_total",
    )
    actions = ("expire", "abandon")

    @admin.action(description="Mark selected sessions as expired")
    def expire(self, request, queryset):
        for session in queryset.filter(status=PracticeSession.Status.IN_PROGRESS):
            if session.mode == PracticeSession.Mode.TIMED:
                session.status = PracticeSession.Status.EXPIRED
                session.save(update_fields=["status"])

    @admin.action(description="Mark selected sessions as abandoned")
    def abandon(self, request, queryset):
        for session in queryset.filter(status=PracticeSession.Status.IN_PROGRESS):
            session.status = PracticeSession.Status.ABANDONED
            session.save(update_fields=["status"])


@admin.register(SessionItem)
class SessionItemAdmin(admin.ModelAdmin):
    list_display = ("session", "question", "display_order")
    search_fields = ("session__id",)
    readonly_fields = (
        "session",
        "question",
        "display_order",
        "snapshot_stem",
        "snapshot_options",
        "snapshot_explanation",
        "snapshot_provenance",
        "snapshot_difficulty",
    )


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("session_item", "selected_choice", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("session_item__session__id",)
    readonly_fields = (
        "session_item",
        "selected_choice",
        "is_correct",
        "answered_at",
        "time_spent_seconds",
    )
