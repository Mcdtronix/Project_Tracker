#!/usr/bin/env python
"""
Debug script to test login functionality
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def debug_login():
    """Debug login functionality"""
    print("🔍 Debugging Login System...")
    
    client = Client()
    
    # Check if any users exist
    user_count = User.objects.count()
    print(f"\n1. Total users in database: {user_count}")
    
    if user_count == 0:
        print("❌ No users found in database!")
        print("Creating a test user...")
        
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created test user: {user.username}")
    else:
        # List existing users
        users = User.objects.all()
        print("Existing users:")
        for user in users:
            print(f"  - {user.username} ({user.email})")
    
    # Test login with test user
    print("\n2. Testing Login...")
    login_data = {
        'username': 'testuser',
        'password': 'TestPass123'
    }
    
    print(f"Attempting login with: {login_data}")
    
    # First, try to get the login page
    response = client.get('/users/login/')
    print(f"GET /users/login/ status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login page accessible")
    else:
        print(f"❌ Login page not accessible: {response.status_code}")
        return
    
    # Now try to login
    response = client.post('/users/login/', login_data)
    print(f"POST /users/login/ status: {response.status_code}")
    
    if response.status_code == 302:
        redirect_url = response.url
        print(f"✅ Login successful! Redirecting to: {redirect_url}")
        
        # Follow the redirect
        response = client.get(redirect_url)
        print(f"Redirect response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Redirect successful")
        else:
            print(f"❌ Redirect failed: {response.status_code}")
    else:
        print(f"❌ Login failed with status: {response.status_code}")
        
        # Check if there are form errors
        if hasattr(response, 'context') and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print("Form errors:")
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"  - {field}: {error}")
    
    # Test authentication
    print("\n3. Testing Authentication...")
    user = User.objects.get(username='testuser')
    is_authenticated = user.is_authenticated
    print(f"User authenticated: {is_authenticated}")
    
    # Test with client session
    client.force_login(user)
    response = client.get('/home/')
    print(f"Accessing /home/ with authenticated user: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Home page accessible for authenticated user")
    else:
        print(f"❌ Home page not accessible: {response.status_code}")
    
    print("\n🎉 Debug Complete!")

if __name__ == '__main__':
    debug_login() 