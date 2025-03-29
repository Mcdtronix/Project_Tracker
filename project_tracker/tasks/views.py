# tasks/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Comprehensive Task ViewSet with advanced filtering
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny,]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Filtering options
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        """
        Filter tasks to show only related projects
        """
        return Task.objects.filter(
            project__owner=self.request.user
        ).select_related('project', 'assigned_to', 'created_by')

    def perform_create(self, serializer):
        """
        Set the task creator to the current user
        """
        serializer.save(created_by=self.request.user)
