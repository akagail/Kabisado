"""Create the exam rows that `accounts.Profile.target_exam` points at.

Only identifiers the profile FK needs are created here; versions, subjects, and
topics come from `manage.py seed_cse_catalogue` so reviewers can inspect them.
"""

from django.db import migrations


def create_cse_exams(apps, schema_editor):
    ExamFamily = apps.get_model("catalog", "ExamFamily")
    Exam = apps.get_model("catalog", "Exam")

    family, _ = ExamFamily.objects.get_or_create(slug="cse", defaults={"name": "Civil Service"})
    Exam.objects.get_or_create(
        family=family,
        slug="cse-professional",
        defaults={"name": "CSE Professional", "level": "professional"},
    )
    Exam.objects.get_or_create(
        family=family,
        slug="cse-subprofessional",
        defaults={"name": "CSE Subprofessional", "level": "subprofessional"},
    )


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_cse_exams, migrations.RunPython.noop),
    ]
