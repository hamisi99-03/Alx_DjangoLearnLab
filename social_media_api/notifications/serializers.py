from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_type', 'target_id', 'created_at', 'is_read']
        read_only_fields = ['actor', 'created_at', 'is_read']