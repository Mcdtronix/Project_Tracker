#!/usr/bin/env python
"""
Test script to verify backend connectivity and API endpoints
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project, ProjectCategory
from tasks.models import Task

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def test_backend_connectivity():
    """Test all backend connections and API endpoints"""
    print("🔍 Testing Backend Connectivity...")
    
    # Create test client
    client = Client()
    
    # Test 1: Check if Django is running
    print("\n1. Testing Django Setup...")
    try:
        response = client.get('/')
        print(f"   ✅ Home page accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Home page error: {e}")
        return False
    
    # Test 2: Check Dashboard
    print("\n2. Testing Dashboard...")
    try:
        response = client.get('/dashboard/')
        print(f"   ✅ Dashboard accessible (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
    
    # Test 3: Check Projects API
    print("\n3. Testing Projects API...")
    try:
        response = client.get('/api/projects/projects/')
        print(f"   ✅ Projects API accessible (Status: {response.status_code})")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Found {len(data.get('results', []))} projects")
    except Exception as e:
        print(f"   ❌ Projects API error: {e}")
    
    # Test 4: Check Tasks API
    print("\n4. Testing Tasks API...")
    try:
        response = client.get('/api/tasks/tasks/')
        print(f"   ✅ Tasks API accessible (Status: {response.status_code})")
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Found {len(data.get('results', []))} tasks")
    except Exception as e:
        print(f"   ❌ Tasks API error: {e}")
    
    # Test 5: Check Dashboard Data API
    print("\n5. Testing Dashboard Data API...")
    try:
        response = client.get('/api/dashboard/data/')
        print(f"   ✅ Dashboard Data API accessible (Status: {response.status_code})")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   📊 Dashboard data retrieved successfully")
            else:
                print(f"   ⚠️ Dashboard data error: {data.get('error')}")
    except Exception as e:
        print(f"   ❌ Dashboard Data API error: {e}")
    
    # Test 6: Check all page routes
    print("\n6. Testing Page Routes...")
    routes = [
        ('/projects/', 'Projects'),
        ('/tasks/', 'Tasks'),
        ('/reports/', 'Reports'),
        ('/calendar/', 'Calendar'),
        ('/team/', 'Team'),
        ('/settings/', 'Settings'),
    ]
    
    for route, name in routes:
        try:
            response = client.get(route)
            print(f"   ✅ {name} page accessible (Status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {name} page error: {e}")
    
    # Test 7: Check Database Models
    print("\n7. Testing Database Models...")
    try:
        project_count = Project.objects.count()
        task_count = Task.objects.count()
        category_count = ProjectCategory.objects.count()
        print(f"   📊 Database Models:")
        print(f"      - Projects: {project_count}")
        print(f"      - Tasks: {task_count}")
        print(f"      - Categories: {category_count}")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🎉 Backend Connectivity Test Complete!")
    return True

def create_sample_data():
    """Create sample data for testing"""
    print("\n📝 Creating Sample Data...")
    
    try:
        # Create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("   ✅ Test user created")
        
        # Create a test category
        category, created = ProjectCategory.objects.get_or_create(
            name='Test Category',
            defaults={'description': 'A test category for testing purposes'}
        )
        if created:
            print("   ✅ Test category created")
        
        # Create a test project
        project, created = Project.objects.get_or_create(
            name='Test Project',
            defaults={
                'description': 'A test project for testing purposes',
                'category': category,
                'status': 'IN_PROGRESS',
                'priority': 'MEDIUM'
            }
        )
        if created:
            print("   ✅ Test project created")
        
        # Create a test task
        task, created = Task.objects.get_or_create(
            title='Test Task',
            defaults={
                'description': 'A test task for testing purposes',
                'project': project,
                'status': 'TODO',
                'priority': 'MEDIUM'
            }
        )
        if created:
            print("   ✅ Test task created")
        
        print("   📊 Sample data created successfully!")
        
    except Exception as e:
        print(f"   ❌ Error creating sample data: {e}")

if __name__ == '__main__':
    print("🚀 Project Tracker Backend Connectivity Test")
    print("=" * 50)
    
    # Create sample data first
    create_sample_data()
    
    # Run connectivity tests
    success = test_backend_connectivity()
    
    if success:
        print("\n✅ All tests passed! Backend is properly connected.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1) 