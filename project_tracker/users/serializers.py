from rest_framework import serializers
from .models import UserSettings
from .models import UserNotification

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'default_project_status', 'default_priority', 'show_completed_tasks', 'enable_templates',
            'theme', 'language', 'date_format', 'refresh_interval', 'items_per_page', 'enable_animations'
        ]

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'message', 'is_read', 'created_at'] 