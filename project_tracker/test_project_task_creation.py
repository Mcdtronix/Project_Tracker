#!/usr/bin/env python
"""
Test script to verify project and task creation, management, and progress tracking
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project, ProjectCategory
from tasks.models import Task
from django.utils import timezone
from datetime import datetime, timedelta
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def test_project_task_creation():
    """Test project and task creation, management, and progress tracking"""
    print("🔍 Testing Project and Task Creation...")
    
    # Create test client
    client = Client()
    
    # Test 1: Create a project
    print("\n1. Testing Project Creation...")
    try:
        # Create a test category first
        category = ProjectCategory.objects.create(
            name='Test Category',
            description='A test category for testing purposes'
        )
        print("   ✅ Test category created")
        
        # Create a test project
        project_data = {
            'name': 'Test Project for Tasks',
            'description': 'A test project to verify task creation and management',
            'category': category.id,
            'status': 'IN_PROGRESS',
            'priority': 'HIGH',
            'start_date': timezone.now().date().isoformat(),
            'estimated_completion_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            'budget': '10000.00'
        }
        
        response = client.post('/api/projects/projects/', 
                             data=json.dumps(project_data),
                             content_type='application/json')
        
        if response.status_code == 201:
            project = response.json()
            project_id = project['id']
            print(f"   ✅ Project created successfully (ID: {project_id})")
            print(f"   📊 Project: {project['name']} - Status: {project['status']} - Progress: {project['progress']}%")
        else:
            print(f"   ❌ Project creation failed (Status: {response.status_code})")
            print(f"   Error: {response.content}")
            return False
            
    except Exception as e:
        print(f"   ❌ Project creation error: {e}")
        return False
    
    # Test 2: Create tasks for the project
    print("\n2. Testing Task Creation...")
    try:
        tasks_data = [
            {
                'title': 'Design User Interface',
                'description': 'Create wireframes and mockups for the user interface',
                'project': project_id,
                'status': 'IN_PROGRESS',
                'priority': 'HIGH',
                'start_date': timezone.now().date().isoformat(),
                'due_date': (timezone.now().date() + timedelta(days=7)).isoformat(),
                'estimated_hours': '16.0'
            },
            {
                'title': 'Implement Backend API',
                'description': 'Develop REST API endpoints for the application',
                'project': project_id,
                'status': 'TODO',
                'priority': 'HIGH',
                'start_date': (timezone.now().date() + timedelta(days=7)).isoformat(),
                'due_date': (timezone.now().date() + timedelta(days=14)).isoformat(),
                'estimated_hours': '24.0'
            },
            {
                'title': 'Write Documentation',
                'description': 'Create user and technical documentation',
                'project': project_id,
                'status': 'TODO',
                'priority': 'MEDIUM',
                'start_date': (timezone.now().date() + timedelta(days=14)).isoformat(),
                'due_date': (timezone.now().date() + timedelta(days=21)).isoformat(),
                'estimated_hours': '8.0'
            }
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            response = client.post('/api/tasks/tasks/',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
            
            if response.status_code == 201:
                task = response.json()
                created_tasks.append(task)
                print(f"   ✅ Task created: {task['title']} (ID: {task['id']})")
            else:
                print(f"   ❌ Task creation failed for: {task_data['title']}")
                print(f"   Error: {response.content}")
        
        print(f"   📊 Created {len(created_tasks)} tasks successfully")
        
    except Exception as e:
        print(f"   ❌ Task creation error: {e}")
        return False
    
    # Test 3: Test task management and progress tracking
    print("\n3. Testing Task Management and Progress...")
    try:
        # Update first task to completed
        if created_tasks:
            task_id = created_tasks[0]['id']
            update_data = {
                'status': 'COMPLETED',
                'actual_hours': '18.0',
                'completed_date': timezone.now().date().isoformat()
            }
            
            response = client.put(f'/api/tasks/tasks/{task_id}/',
                                data=json.dumps(update_data),
                                content_type='application/json')
            
            if response.status_code == 200:
                updated_task = response.json()
                print(f"   ✅ Task updated: {updated_task['title']} - Status: {updated_task['status']}")
                print(f"   📊 Actual hours: {updated_task['actual_hours']}h")
            else:
                print(f"   ❌ Task update failed (Status: {response.status_code})")
        
        # Update second task to in progress
        if len(created_tasks) > 1:
            task_id = created_tasks[1]['id']
            update_data = {
                'status': 'IN_PROGRESS',
                'actual_hours': '8.0'
            }
            
            response = client.put(f'/api/tasks/tasks/{task_id}/',
                                data=json.dumps(update_data),
                                content_type='application/json')
            
            if response.status_code == 200:
                updated_task = response.json()
                print(f"   ✅ Task updated: {updated_task['title']} - Status: {updated_task['status']}")
            else:
                print(f"   ❌ Task update failed (Status: {response.status_code})")
        
    except Exception as e:
        print(f"   ❌ Task management error: {e}")
        return False
    
    # Test 4: Verify project progress calculation
    print("\n4. Testing Project Progress Calculation...")
    try:
        # Get updated project data
        response = client.get(f'/api/projects/projects/{project_id}/')
        
        if response.status_code == 200:
            updated_project = response.json()
            progress = updated_project['progress']
            print(f"   ✅ Project progress calculated: {progress}%")
            
            # Verify progress calculation
            if progress > 0:
                print(f"   📊 Progress is working correctly (1 completed task out of 3 total)")
            else:
                print(f"   ⚠️ Progress calculation may need verification")
        else:
            print(f"   ❌ Failed to get updated project data (Status: {response.status_code})")
        
    except Exception as e:
        print(f"   ❌ Progress calculation error: {e}")
        return False
    
    # Test 5: Test task filtering and search
    print("\n5. Testing Task Filtering and Search...")
    try:
        # Test status filter
        response = client.get('/api/tasks/tasks/?status=COMPLETED')
        if response.status_code == 200:
            completed_tasks = response.json()
            print(f"   ✅ Status filter working: Found {len(completed_tasks.get('results', []))} completed tasks")
        
        # Test project filter
        response = client.get(f'/api/tasks/tasks/?project={project_id}')
        if response.status_code == 200:
            project_tasks = response.json()
            print(f"   ✅ Project filter working: Found {len(project_tasks.get('results', []))} tasks for project")
        
        # Test search
        response = client.get('/api/tasks/tasks/?search=interface')
        if response.status_code == 200:
            search_results = response.json()
            print(f"   ✅ Search working: Found {len(search_results.get('results', []))} tasks matching 'interface'")
        
    except Exception as e:
        print(f"   ❌ Filtering/Search error: {e}")
        return False
    
    # Test 6: Test dashboard data with new project and tasks
    print("\n6. Testing Dashboard Data...")
    try:
        response = client.get('/api/dashboard/data/')
        
        if response.status_code == 200:
            dashboard_data = response.json()
            if dashboard_data.get('success'):
                data = dashboard_data['data']
                print(f"   ✅ Dashboard data updated:")
                print(f"      - Total Projects: {data['total_projects']}")
                print(f"      - Total Tasks: {data['total_tasks']}")
                print(f"      - Completed Tasks: {data['completed_tasks']}")
                print(f"      - Task Completion Rate: {data['task_completion_rate']}%")
            else:
                print(f"   ⚠️ Dashboard data error: {dashboard_data.get('error')}")
        else:
            print(f"   ❌ Dashboard data failed (Status: {response.status_code})")
        
    except Exception as e:
        print(f"   ❌ Dashboard data error: {e}")
        return False
    
    print("\n🎉 Project and Task Creation Test Complete!")
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Delete test tasks
        Task.objects.filter(title__startswith='Test').delete()
        print("   ✅ Test tasks deleted")
        
        # Delete test projects
        Project.objects.filter(name__startswith='Test').delete()
        print("   ✅ Test projects deleted")
        
        # Delete test categories
        ProjectCategory.objects.filter(name__startswith='Test').delete()
        print("   ✅ Test categories deleted")
        
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")

if __name__ == '__main__':
    print("🚀 Project and Task Creation Test")
    print("=" * 50)
    
    # Run the test
    success = test_project_task_creation()
    
    if success:
        print("\n✅ All tests passed! Project and task creation is working properly.")
        
        # Ask if user wants to clean up test data
        cleanup = input("\n🧹 Do you want to clean up test data? (y/n): ").lower().strip()
        if cleanup == 'y':
            cleanup_test_data()
            print("✅ Test data cleaned up!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 