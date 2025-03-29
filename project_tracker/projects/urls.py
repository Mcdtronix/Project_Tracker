# projects/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectCategoryViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-categories', ProjectCategoryViewSet, basename='project-category')

urlpatterns = [
    path('', include(router.urls)),
]