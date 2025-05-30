# projects/serializers.py
from rest_framework import serializers
from .models import Project, ProjectCategory

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    """
    Comprehensive Project Serializer
    """
    progress = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    category = ProjectCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(), 
        source='category', 
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 
            'category', 'category_id', 'status', 'priority', 
            'start_date', 'end_date', 'estimated_completion_date', 
            'budget', 'current_spend', 'created_at', 'updated_at', 
            'progress', 'is_overdue'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_progress(self, obj):
        return obj.calculate_progress()

    def get_is_overdue(self, obj):
        return obj.is_overdue()