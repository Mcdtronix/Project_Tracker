# tasks/serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Comprehensive Task Serializer
    """
    is_overdue = serializers.SerializerMethodField()
    project_name = serializers.CharField(
        source='project.name', 
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 
            'project', 'project_name', 
            'status', 'priority', 
            'start_date', 'due_date', 'completed_date',
            'estimated_hours', 'actual_hours',
            'created_at', 'updated_at', 
            'is_overdue'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_is_overdue(self, obj):
        return obj.is_overdue()