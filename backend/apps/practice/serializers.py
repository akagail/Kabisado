from __future__ import annotations

from rest_framework import serializers


class PracticeSessionStartSerializer(serializers.Serializer):
    topic = serializers.UUIDField()
    mode = serializers.ChoiceField(choices=["untimed", "timed"])
    size = serializers.IntegerField(min_value=1, max_value=50, default=20)


class ChoiceSnapshotSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    is_correct = serializers.BooleanField()


class PracticeSessionDetailSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    mode = serializers.ChoiceField(choices=["untimed", "timed"])
    status = serializers.ChoiceField(choices=["in_progress", "submitted", "expired", "abandoned"])
    time_limit_seconds = serializers.IntegerField(allow_null=True)
    started_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField(allow_null=True)
    submitted_at = serializers.DateTimeField(allow_null=True)
    score_correct = serializers.IntegerField(allow_null=True)
    score_total = serializers.IntegerField(allow_null=True)
    items = serializers.SerializerMethodField()

    def get_items(self, obj) -> list[dict]:
        submitted = obj.status == "submitted"
        result = []
        for item in obj.items.all():
            answer = item.answers.first()
            options = item.snapshot_options
            if not submitted:
                options = [{"id": o["id"], "text": o["text"]} for o in options]
            result.append(
                {
                    "position": item.display_order,
                    "question": {
                        "id": str(item.question_id),
                        "stem": item.snapshot_stem,
                        "options": options,
                    },
                    "saved_answer": (
                        {"selected_option_id": str(answer.selected_choice_id)}
                        if answer and answer.selected_choice_id
                        else None
                    ),
                }
            )
        return result


class PracticeSessionSaveAnswerSerializer(serializers.Serializer):
    selected_option_id = serializers.UUIDField(allow_null=True)


class PracticeSessionSubmitSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=["in_progress", "submitted", "expired", "abandoned"])
    submitted_at = serializers.DateTimeField(allow_null=True)
    score_correct = serializers.IntegerField(allow_null=True)
    score_total = serializers.IntegerField(allow_null=True)


class PracticeSessionResultsSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    score_correct = serializers.IntegerField()
    score_total = serializers.IntegerField()
    items = serializers.ListField()


class PracticeSessionHistorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=["in_progress", "submitted", "expired", "abandoned"])
    mode = serializers.ChoiceField(choices=["untimed", "timed"])
    started_at = serializers.DateTimeField()
    submitted_at = serializers.DateTimeField(allow_null=True)
    score_correct = serializers.IntegerField(allow_null=True)
    score_total = serializers.IntegerField(allow_null=True)
