# tasks/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Comprehensive Task ViewSet with advanced filtering
    """
    queryset = Task.objects.all().select_related('project')
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny,]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Filtering options
    filterset_fields = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def perform_create(self, serializer):
        """
        Set the task creator to the current user
        """
        serializer.save(created_by=self.request.user)
