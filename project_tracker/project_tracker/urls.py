"""
URL configuration for project_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from rest_framework import permissions
from . import views
from django.contrib.auth import views as auth_views
from .views import landing

schema_view = get_schema_view(
   openapi.Info(
      title="Projects tracker API",
      default_version='v1',
      description="API for Projects Tracker",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', landing, name='landing'),
    # User authentication URLs
    path('users/', include('users.urls')),
    # Home page
    path('home/', views.home, name='home'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/dashboard/data/', views.dashboard_data, name='dashboard_data'),
    
    # Page routes
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/', views.tasks, name='tasks'),
    path('reports/', views.reports, name='reports'),
    path('calendar/', views.calendar, name='calendar'),
    path('team/', views.team, name='team'),
    path('settings/', views.settings, name='settings'),
    
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # App-specific URLs
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/recent-activity/', views.recent_activity, name='recent-activity'),

    #  Documentations
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
