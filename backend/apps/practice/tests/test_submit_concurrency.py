from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor

import pytest
from django.core.management import call_command
from django.db import connection, connections

from apps.accounts.models import User
from apps.catalog.models import Topic
from apps.core.models import AuditEvent
from apps.practice import services
from apps.questions.models import Question

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.skipif(connection.vendor != "postgresql", reason="row locking requires PostgreSQL")
def test_concurrent_submit_scores_once():
    call_command("seed_cse_catalogue", force=True)
    topic = Topic.objects.get(
        subject__exam_version__exam__slug="cse-professional", slug="word-meaning"
    )
    user = User.objects.create_user(email="learner@example.com", password="CorrectHorse123!")
    Question.objects.create(
        topic=topic,
        stem="What is 2 + 2?",
        stem_hash="concurrency-test",
        author=user,
        status=Question.Status.PUBLISHED,
    )
    session = services.start_session(user, mode="untimed", topic_identifier=str(topic.pk), size=1)

    barrier = threading.Barrier(2)

    def submit():
        barrier.wait()
        try:
            return services.submit_session(user, session.id)
        finally:
            connections.close_all()

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda _: submit(), range(2)))

    session.refresh_from_db()
    assert session.status == "submitted"
    assert (
        AuditEvent.objects.filter(
            action=AuditEvent.Action.PRACTICE_SESSION_SUBMITTED, object_id=session.id
        ).count()
        == 1
    )
