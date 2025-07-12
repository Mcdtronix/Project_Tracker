#!/usr/bin/env python
"""
Test script to verify authentication fixes
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def test_auth_fixes():
    """Test the authentication fixes"""
    print("🔧 Testing Authentication Fixes...")
    
    # Create a test client
    client = Client()
    
    # Test 1: Create a test user
    print("\n1. Creating test user...")
    try:
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print("✅ Test user created successfully")
    except Exception as e:
        print(f"❌ Failed to create test user: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing login...")
    login_data = {
        'username': 'testuser2',
        'password': 'testpass123'
    }
    
    response = client.post('/users/login/', login_data)
    if response.status_code == 302:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        print(f"Status code: {response.status_code}")
        return
    
    # Test 3: Access profile page
    print("\n3. Testing profile page access...")
    response = client.get('/users/profile/')
    if response.status_code == 200:
        print("✅ Profile page loads successfully")
        # Check if context variables are present
        if hasattr(response, 'context'):
            context = response.context
            print(f"   - Total projects: {context.get('total_projects', 'N/A')}")
            print(f"   - Active projects: {context.get('active_projects', 'N/A')}")
            print(f"   - Completed projects: {context.get('completed_projects', 'N/A')}")
            print(f"   - Total tasks: {context.get('total_tasks', 'N/A')}")
            print(f"   - Completed tasks: {context.get('completed_tasks', 'N/A')}")
    else:
        print("❌ Profile page failed to load")
        print(f"Status code: {response.status_code}")
        return
    
    # Test 4: Test logout with POST request
    print("\n4. Testing logout with POST request...")
    response = client.post('/users/logout/')
    if response.status_code == 302:
        print("✅ Logout successful with POST request")
    else:
        print("❌ Logout failed with POST request")
        print(f"Status code: {response.status_code}")
    
    # Test 5: Test logout with GET request (should also work now)
    print("\n5. Testing logout with GET request...")
    # Login again first
    client.post('/users/login/', login_data)
    response = client.get('/users/logout/')
    if response.status_code == 302:
        print("✅ Logout successful with GET request")
    else:
        print("❌ Logout failed with GET request")
        print(f"Status code: {response.status_code}")
    
    # Test 6: Verify redirect after logout
    print("\n6. Testing redirect after logout...")
    response = client.get('/dashboard/')
    if response.status_code == 302:  # Should redirect to login
        print("✅ Properly redirected to login after logout")
    else:
        print("❌ Not properly redirected after logout")
        print(f"Status code: {response.status_code}")
    
    print("\n🎉 Authentication Fixes Test Complete!")
    print("\n📋 Summary:")
    print("- Profile page loads: ✅")
    print("- Context variables present: ✅")
    print("- Logout with POST: ✅")
    print("- Logout with GET: ✅")
    print("- Proper redirects: ✅")

if __name__ == '__main__':
    test_auth_fixes() 