from __future__ import annotations

from django.contrib import admin, messages
from rest_framework.exceptions import APIException

from apps.questions import services
from apps.questions.models import Choice, ContentFlag, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    can_delete = False
    readonly_fields = ("text", "is_correct", "rationale", "display_order")

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Read-only detail; workflow actions go through the services (and audit)."""

    list_display = ("summary", "topic", "status", "difficulty", "author", "reviewer", "updated_at")
    list_filter = ("status", "difficulty", "topic__subject__exam_version__exam")
    search_fields = ("stem", "explanation")
    readonly_fields = (
        "id",
        "topic",
        "stem",
        "stem_hash",
        "explanation",
        "provenance",
        "difficulty",
        "status",
        "origin",
        "author",
        "reviewer",
        "reviewed_at",
        "created_at",
        "updated_at",
    )
    inlines = [ChoiceInline]
    actions = ("submit_for_review", "approve", "reject", "retire")

    def summary(self, obj: Question) -> str:
        return str(obj)

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.action(description="Submit selected drafts for review")
    def submit_for_review(self, request, queryset):
        self._run(
            request, queryset.filter(status=Question.Status.DRAFT), services.submit_for_review
        )

    @admin.action(description="Publish selected in-review items")
    def approve(self, request, queryset):
        self._run(
            request,
            queryset.filter(status=Question.Status.IN_REVIEW),
            lambda actor, question: services.review_question(actor, question, approve=True),
        )

    @admin.action(description="Reject selected in-review items")
    def reject(self, request, queryset):
        self._run(
            request,
            queryset.filter(status=Question.Status.IN_REVIEW),
            lambda actor, question: services.review_question(actor, question, approve=False),
        )

    @admin.action(description="Retire selected published items")
    def retire(self, request, queryset):
        self._run(
            request,
            queryset.filter(status=Question.Status.PUBLISHED),
            services.retire_question,
        )

    def _run(self, request, queryset, action) -> None:
        updated = 0
        for question in queryset:
            try:
                action(request.user, question)
                updated += 1
            except APIException as exc:
                self.message_user(request, f"{question}: {exc.detail}", messages.ERROR)
        self.message_user(request, f"{updated} item(s) updated.")


@admin.register(ContentFlag)
class ContentFlagAdmin(admin.ModelAdmin):
    list_display = ("question", "reason", "status", "reporter", "created_at", "resolved_by")
    list_filter = ("status", "reason")
    search_fields = ("question__stem", "note")
    readonly_fields = (
        "id",
        "question",
        "reporter",
        "reason",
        "note",
        "status",
        "resolved_by",
        "resolved_at",
        "resolution_note",
        "created_at",
        "updated_at",
    )
    actions = ("resolve", "dismiss")

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.action(description="Resolve selected open flags")
    def resolve(self, request, queryset):
        self._close(request, queryset, dismiss=False)

    @admin.action(description="Dismiss selected open flags")
    def dismiss(self, request, queryset):
        self._close(request, queryset, dismiss=True)

    def _close(self, request, queryset, *, dismiss: bool) -> None:
        updated = 0
        for flag in queryset.filter(status=ContentFlag.Status.OPEN):
            services.resolve_flag(request.user, flag, dismiss=dismiss)
            updated += 1
        self.message_user(request, f"{updated} flag(s) updated.")
