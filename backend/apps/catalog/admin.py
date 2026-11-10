from django.contrib import admin

from apps.catalog.models import Exam, ExamFamily, ExamVersion, Subject, Topic


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 0


@admin.register(ExamFamily)
class ExamFamilyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    inlines = [ExamInline]


class ExamVersionInline(admin.TabularInline):
    model = ExamVersion
    extra = 0


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "family", "level", "is_active")
    list_filter = ("family", "level", "is_active")
    search_fields = ("name", "slug")
    inlines = [ExamVersionInline]


@admin.register(ExamVersion)
class ExamVersionAdmin(admin.ModelAdmin):
    list_display = ("label", "exam", "published_at", "source_url", "is_active")
    list_filter = ("exam", "is_active")
    search_fields = ("label", "exam__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "exam_version", "slug", "display_order")
    list_filter = ("exam_version__exam",)
    search_fields = ("name", "slug")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "parent", "slug", "display_order")
    list_filter = ("subject__exam_version__exam",)
    search_fields = ("name", "slug")
