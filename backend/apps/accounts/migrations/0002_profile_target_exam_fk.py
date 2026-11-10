"""Replace the temporary `target_exam` slug with a FK to `catalog.Exam` (KAB-102)."""

from django.db import migrations, models
import django.db.models.deletion

SLUG_MAP = {
    "professional": "cse-professional",
    "subprofessional": "cse-subprofessional",
}


def slug_to_fk(apps, schema_editor):
    Profile = apps.get_model("accounts", "Profile")
    Exam = apps.get_model("catalog", "Exam")

    for old_slug, exam_slug in SLUG_MAP.items():
        try:
            exam = Exam.objects.get(slug=exam_slug)
        except Exam.DoesNotExist:
            continue
        Profile.objects.filter(target_exam_old=old_slug).update(target_exam=exam)


def fk_to_slug(apps, schema_editor):
    Profile = apps.get_model("accounts", "Profile")
    reverse = {exam: old for old, exam in SLUG_MAP.items()}

    for profile in Profile.objects.select_related("target_exam").all():
        if profile.target_exam_id and profile.target_exam.slug in reverse:
            Profile.objects.filter(pk=profile.pk).update(
                target_exam_old=reverse[profile.target_exam.slug]
            )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("catalog", "0002_seed_exam_identity"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="target_exam",
            new_name="target_exam_old",
        ),
        migrations.AddField(
            model_name="profile",
            name="target_exam",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="targeted_by_profiles",
                to="catalog.exam",
            ),
        ),
        migrations.RunPython(slug_to_fk, fk_to_slug),
        migrations.RemoveField(
            model_name="profile",
            name="target_exam_old",
        ),
    ]
