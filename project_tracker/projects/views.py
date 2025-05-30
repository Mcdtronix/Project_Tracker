# projects/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, ProjectCategory
from .serializers import ProjectSerializer, ProjectCategorySerializer

class ProjectCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project Categories
    """
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [permissions.AllowAny,]

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Comprehensive Project ViewSet with advanced filtering
    """
    queryset = Project.objects.all().prefetch_related('category')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny,]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Filtering options
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date']

    def perform_create(self, serializer):
        """
        Set the project owner to the current user
        """
        serializer.save(owner=self.request.user)