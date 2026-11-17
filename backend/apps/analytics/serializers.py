from __future__ import annotations

from rest_framework import serializers


class AnalyticsSubjectSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()


class SubjectAccuracySerializer(serializers.Serializer):
    subject = AnalyticsSubjectSerializer()
    accuracy = serializers.FloatField()
    attempts = serializers.IntegerField()


class SubjectAnalyticsSerializer(serializers.Serializer):
    subjects = SubjectAccuracySerializer(many=True)


class AnalyticsTopicSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    slug = serializers.CharField()
    name = serializers.CharField()


class TopicAccuracySerializer(serializers.Serializer):
    topic = AnalyticsTopicSerializer()
    accuracy = serializers.FloatField()
    attempts = serializers.IntegerField()
    weak_topic = serializers.BooleanField()
    weak_reason = serializers.CharField(allow_null=True)


class TopicAnalyticsSerializer(serializers.Serializer):
    topics = TopicAccuracySerializer(many=True)
