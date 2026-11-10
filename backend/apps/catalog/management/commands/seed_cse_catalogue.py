"""Seed the CSE catalogue from the verified official coverage areas.

Source: docs/product/cse-exam-reference.md (Announcement No. 06, s. 2026).
Re-verify the CSC bulletin before running against a new environment.
"""

from __future__ import annotations

import datetime as dt

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.catalog.models import Exam, ExamFamily, ExamVersion, Subject, Topic

FAMILY = {"slug": "cse", "name": "Civil Service"}

VERSION = {
    "slug": "2027-bulletin",
    "label": "14 March 2027 CSE-PPT (Announcement No. 06, s. 2026)",
    "source_url": (
        "https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/"
        "ExamAnn_2026_06_Conduct%20of%2014%20March%202027%20CSE-PPT%20orig%20signed.pdf"
    ),
    "published_at": dt.date(2026, 10, 21),
    "accessed_at": dt.date(2026, 11, 6),
    # Item count and time limit are not published for this version (reference §5).
    "passing_rate": "80.00",
}

GENERAL_INFORMATION = {
    "slug": "general-information",
    "name": "General Information",
    "topics": [
        ("philippine-constitution", "Philippine Constitution"),
        (
            "code-of-conduct-ra-6713",
            "Code of Conduct and Ethical Standards for Public Officials and Employees (R.A. 6713)",
        ),
        ("peace-and-human-rights", "Peace and Human Rights Issues and Concepts"),
        ("environment-management", "Environment Management and Protection"),
    ],
}

VERBAL_ABILITY = {
    "slug": "verbal-ability",
    "name": "Verbal Ability",
    "topics": [
        ("word-meaning", "Word Meaning"),
        ("sentence-completion", "Sentence Completion"),
        ("error-recognition", "Error Recognition"),
        ("sentence-structure", "Sentence Structure"),
        ("paragraph-organization", "Paragraph Organization"),
        ("reading-comprehension", "Reading Comprehension"),
    ],
}

NUMERICAL_ABILITY = {
    "slug": "numerical-ability",
    "name": "Numerical Ability",
    "topics": [
        ("basic-operations", "Basic Operations"),
        ("number-sequence", "Number Sequence"),
        ("word-problems", "Word Problems"),
    ],
}

ANALYTICAL_ABILITY = {
    "slug": "analytical-ability",
    "name": "Analytical Ability",
    "topics": [
        ("word-analogy", "Word Analogy"),
        ("symbolic-logic", "Symbolic Logic / Abstract Reasoning"),
        ("identifying-assumptions", "Identifying Assumptions and Drawing Conclusions"),
        ("data-interpretation", "Data Interpretation"),
    ],
}

CLERICAL_ABILITY = {
    "slug": "clerical-ability",
    "name": "Clerical Ability",
    "topics": [("filing", "Filing"), ("spelling", "Spelling")],
}

EXAMS = [
    {
        "slug": "cse-professional",
        "name": "CSE Professional",
        "level": Exam.Level.PROFESSIONAL,
        "subjects": [
            GENERAL_INFORMATION,
            VERBAL_ABILITY,
            NUMERICAL_ABILITY,
            ANALYTICAL_ABILITY,
        ],
    },
    {
        "slug": "cse-subprofessional",
        "name": "CSE Subprofessional",
        "level": Exam.Level.SUBPROFESSIONAL,
        "subjects": [
            GENERAL_INFORMATION,
            VERBAL_ABILITY,
            NUMERICAL_ABILITY,
            CLERICAL_ABILITY,
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the CSE catalogue. Idempotent; re-running adds nothing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Run even when DEBUG is off (re-verify the CSC bulletin first).",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to seed outside DEBUG. Re-verify the CSC bulletin, "
                "then re-run with --force."
            )

        family, _ = ExamFamily.objects.get_or_create(
            slug=FAMILY["slug"], defaults={"name": FAMILY["name"]}
        )
        created = 0

        for exam_data in EXAMS:
            exam, _ = Exam.objects.get_or_create(
                family=family,
                slug=exam_data["slug"],
                defaults={"name": exam_data["name"], "level": exam_data["level"]},
            )
            version, _ = ExamVersion.objects.get_or_create(
                exam=exam, slug=VERSION["slug"], defaults=VERSION
            )
            for subject_order, subject_data in enumerate(exam_data["subjects"]):
                subject, _ = Subject.objects.get_or_create(
                    exam_version=version,
                    slug=subject_data["slug"],
                    defaults={"name": subject_data["name"], "display_order": subject_order},
                )
                for topic_order, (slug, name) in enumerate(subject_data["topics"]):
                    _, topic_created = Topic.objects.get_or_create(
                        subject=subject,
                        parent=None,
                        slug=slug,
                        defaults={"name": name, "display_order": topic_order},
                    )
                    created += int(topic_created)
            self.stdout.write(f"{exam.name}: {version.label}")

        self.stdout.write(self.style.SUCCESS(f"Catalogue ready. {created} new topics added."))
