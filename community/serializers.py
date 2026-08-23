# community/serializers.py
from rest_framework import serializers
from accounts.models import StudyRecord

class StudyRecordSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = StudyRecord
        fields = [
            'id',
            'username',
            'subject',
            'duration_minutes',
            'memo',
            'likes_count',
            'created_at',
        ]