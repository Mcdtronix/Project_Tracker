from django.shortcuts import render
from django.http import JsonResponse
from projects.models import Project
from tasks.models import Task
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def dashboard(request):
    """Interactive dashboard with real-time data and charts"""
    try:
        # Get current date and calculate date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Get project statistics
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status='IN_PROGRESS').count()
        completed_projects = Project.objects.filter(status='COMPLETED').count()
        overdue_projects = Project.objects.filter(
            estimated_completion_date__lt=today,
            status__in=['PLANNING', 'IN_PROGRESS']
        ).count()
        
        # Get task statistics
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='COMPLETED').count()
        pending_tasks = Task.objects.filter(status='TODO').count()
        overdue_tasks = Task.objects.filter(
            due_date__lt=today,
            status__in=['TODO', 'IN_PROGRESS']
        ).count()
        
        # Get recent projects
        recent_projects = Project.objects.order_by('-created_at')[:5]
        
        # Get recent tasks
        recent_tasks = Task.objects.select_related('project').order_by('-created_at')[:10]
        
        # Get tasks by status for chart
        tasks_by_status = {
            'TODO': Task.objects.filter(status='TODO').count(),
            'IN_PROGRESS': Task.objects.filter(status='IN_PROGRESS').count(),
            'REVIEW': Task.objects.filter(status='REVIEW').count(),
            'COMPLETED': Task.objects.filter(status='COMPLETED').count(),
            'BLOCKED': Task.objects.filter(status='BLOCKED').count(),
        }
        
        # Get projects by status for chart
        projects_by_status = {
            'PLANNING': Project.objects.filter(status='PLANNING').count(),
            'IN_PROGRESS': Project.objects.filter(status='IN_PROGRESS').count(),
            'ON_HOLD': Project.objects.filter(status='ON_HOLD').count(),
            'COMPLETED': Project.objects.filter(status='COMPLETED').count(),
            'CANCELLED': Project.objects.filter(status='CANCELLED').count(),
        }
        
        # Calculate completion rates
        project_completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Get weekly progress data
        weekly_data = []
        for i in range(7):
            date = today - timedelta(days=i)
            tasks_completed = Task.objects.filter(
                completed_date=date,
                status='COMPLETED'
            ).count()
            weekly_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%a'),
                'completed': tasks_completed
            })
        weekly_data.reverse()
        
        context = {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'overdue_projects': overdue_projects,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'recent_projects': recent_projects,
            'recent_tasks': recent_tasks,
            'tasks_by_status': tasks_by_status,
            'projects_by_status': projects_by_status,
            'project_completion_rate': round(project_completion_rate, 1),
            'task_completion_rate': round(task_completion_rate, 1),
            'weekly_data': weekly_data,
        }
        
        return render(request, 'dashboard.html', context)
    except Exception as e:
        # Return error context if there's an issue
        context = {
            'total_projects': 0,
            'active_projects': 0,
            'completed_projects': 0,
            'overdue_projects': 0,
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'overdue_tasks': 0,
            'recent_projects': [],
            'recent_tasks': [],
            'tasks_by_status': {'TODO': 0, 'IN_PROGRESS': 0, 'REVIEW': 0, 'COMPLETED': 0, 'BLOCKED': 0},
            'projects_by_status': {'PLANNING': 0, 'IN_PROGRESS': 0, 'ON_HOLD': 0, 'COMPLETED': 0, 'CANCELLED': 0},
            'project_completion_rate': 0,
            'task_completion_rate': 0,
            'weekly_data': [],
            'error_message': str(e)
        }
        return render(request, 'dashboard.html', context)

def projects(request):
    """Projects page view"""
    return render(request, 'projects.html')

def tasks(request):
    """Tasks page view"""
    return render(request, 'tasks.html')

def reports(request):
    """Reports page view"""
    return render(request, 'reports.html')

def calendar(request):
    """Calendar page view"""
    return render(request, 'calendar.html')

def team(request):
    """Team page view"""
    return render(request, 'team.html')

def settings(request):
    """Settings page view"""
    return render(request, 'settings.html')

@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data(request):
    """API endpoint for dashboard data updates"""
    try:
        if request.method == 'GET':
            # Get real-time statistics
            total_projects = Project.objects.count()
            active_projects = Project.objects.filter(status='IN_PROGRESS').count()
            total_tasks = Task.objects.count()
            completed_tasks = Task.objects.filter(status='COMPLETED').count()
            
            # Get recent activity
            recent_projects = Project.objects.order_by('-created_at')[:3]
            recent_tasks = Task.objects.select_related('project').order_by('-created_at')[:5]
            
            # Calculate completion rates
            project_completion_rate = (active_projects / total_projects * 100) if total_projects > 0 else 0
            task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            return JsonResponse({
                'success': True,
                'data': {
                    'total_projects': total_projects,
                    'active_projects': active_projects,
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'project_completion_rate': round(project_completion_rate, 1),
                    'task_completion_rate': round(task_completion_rate, 1),
                    'recent_projects': [
                        {
                            'id': p.id,
                            'name': p.name,
                            'status': p.status,
                            'progress': p.calculate_progress()
                        } for p in recent_projects
                    ],
                    'recent_tasks': [
                        {
                            'id': t.id,
                            'title': t.title,
                            'status': t.status,
                            'project_name': t.project.name
                        } for t in recent_tasks
                    ]
                },
                'timestamp': timezone.now().isoformat()
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': {
                'total_projects': 0,
                'active_projects': 0,
                'total_tasks': 0,
                'completed_tasks': 0,
                'project_completion_rate': 0,
                'task_completion_rate': 0,
                'recent_projects': [],
                'recent_tasks': []
            },
            'timestamp': timezone.now().isoformat()
        }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400) 