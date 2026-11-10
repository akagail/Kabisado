from __future__ import annotations

from rest_framework import serializers

from apps.questions.models import ContentFlag, Question


def choice_payload(choice, *, include_answer: bool) -> dict:
    data = {
        "id": str(choice.pk),
        "text": choice.text,
        "display_order": choice.display_order,
    }
    if include_answer:
        data["is_correct"] = choice.is_correct
        data["rationale"] = choice.rationale
    return data


def question_payload(question: Question, *, include_answer: bool) -> dict:
    """Staff see the key and provenance; learners never receive the answer."""
    data = {
        "id": str(question.pk),
        "topic": str(question.topic_id),
        "stem": question.stem,
        "difficulty": question.difficulty,
        "status": question.status,
        "options": [
            choice_payload(choice, include_answer=include_answer)
            for choice in question.choices.all()
        ],
    }
    if include_answer:
        data.update(
            {
                "explanation": question.explanation,
                "provenance": question.provenance,
                "origin": question.origin,
                "author_id": str(question.author_id),
                "reviewer_id": str(question.reviewer_id) if question.reviewer_id else None,
                "reviewed_at": question.reviewed_at.isoformat() if question.reviewed_at else None,
                "created_at": question.created_at.isoformat(),
                "updated_at": question.updated_at.isoformat(),
            }
        )
    return data


def flag_payload(flag: ContentFlag) -> dict:
    return {
        "id": str(flag.pk),
        "question_id": str(flag.question_id),
        "reason": flag.reason,
        "note": flag.note,
        "status": flag.status,
        "created_at": flag.created_at.isoformat(),
        "resolved_at": flag.resolved_at.isoformat() if flag.resolved_at else None,
        "resolution_note": flag.resolution_note,
    }


class OptionInputSerializer(serializers.Serializer):
    text = serializers.CharField()
    rationale = serializers.CharField()


class QuestionCreateSerializer(serializers.Serializer):
    topic = serializers.UUIDField()
    stem = serializers.CharField()
    options = OptionInputSerializer(many=True)
    correct_answer_index = serializers.IntegerField(min_value=0)
    explanation = serializers.CharField(required=False, allow_blank=True, default="")
    provenance = serializers.CharField(required=False, allow_blank=True, default="")
    difficulty = serializers.IntegerField(min_value=1, max_value=5, default=3)


class QuestionReviewSerializer(serializers.Serializer):
    approve = serializers.BooleanField()
    reason = serializers.CharField(required=False, allow_blank=True, default="")


class QuestionRetireSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True, default="")


class FlagCreateSerializer(serializers.Serializer):
    reason = serializers.ChoiceField(choices=ContentFlag.Reason.choices)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class ChoiceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    is_correct = serializers.BooleanField()
    rationale = serializers.CharField()
    display_order = serializers.IntegerField()


class LearnerChoiceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    display_order = serializers.IntegerField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    topic = serializers.UUIDField()
    stem = serializers.CharField()
    difficulty = serializers.IntegerField()
    status = serializers.CharField()
    options = ChoiceSerializer(many=True)
    explanation = serializers.CharField()
    provenance = serializers.CharField()
    origin = serializers.CharField()
    author_id = serializers.UUIDField()
    reviewer_id = serializers.UUIDField(allow_null=True)
    reviewed_at = serializers.DateTimeField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class LearnerQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    topic = serializers.UUIDField()
    stem = serializers.CharField()
    difficulty = serializers.IntegerField()
    status = serializers.CharField()
    options = LearnerChoiceSerializer(many=True)


class QuestionEnvelopeSerializer(serializers.Serializer):
    question = QuestionSerializer()


class QuestionStatusSerializer(serializers.Serializer):
    question = QuestionSerializer()
    status = serializers.CharField()


class ContentFlagSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    question_id = serializers.UUIDField()
    reason = serializers.CharField()
    note = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    resolved_at = serializers.DateTimeField(allow_null=True)
    resolution_note = serializers.CharField()


class ContentFlagEnvelopeSerializer(serializers.Serializer):
    flag = ContentFlagSerializer()


class FlagReporterSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class FlagQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    stem = serializers.CharField()
    status = serializers.CharField()


class FlagQueueItemSerializer(serializers.Serializer):
    flag = ContentFlagSerializer()
    reporter = FlagReporterSerializer(allow_null=True)
    question = FlagQuestionSerializer()
