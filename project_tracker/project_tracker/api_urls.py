from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet, ProjectCategoryViewSet
from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-categories', ProjectCategoryViewSet, basename='project-category')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls 