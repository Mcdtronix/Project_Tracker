#!/usr/bin/env python
"""
Test script to verify login redirect functionality
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def test_login_redirect():
    """Test that login redirects to home page"""
    print("🔍 Testing Login Redirect...")
    
    client = Client()
    
    # Create a test user
    user = User.objects.create_user(
        username='testuser_redirect',
        email='testredirect@example.com',
        password='SecurePass123',
        first_name='Test',
        last_name='User'
    )
    
    # Test login redirect
    print("\n1. Testing Login Redirect...")
    login_data = {
        'username': 'testuser_redirect',
        'password': 'SecurePass123'
    }
    
    response = client.post('/users/login/', login_data)
    
    if response.status_code == 302:
        redirect_url = response.url
        print(f"✅ Login successful, redirecting to: {redirect_url}")
        
        if redirect_url == '/home/':
            print("✅ Login correctly redirects to home page")
        else:
            print(f"❌ Login redirects to {redirect_url}, expected /home/")
    else:
        print(f"❌ Login failed with status code: {response.status_code}")
    
    # Test registration redirect
    print("\n2. Testing Registration Redirect...")
    register_data = {
        'username': 'newuser_redirect',
        'email': 'newredirect@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'password1': 'SecurePass123',
        'password2': 'SecurePass123'
    }
    
    response = client.post('/users/register/', register_data)
    
    if response.status_code == 302:
        redirect_url = response.url
        print(f"✅ Registration successful, redirecting to: {redirect_url}")
        
        if redirect_url == '/home/':
            print("✅ Registration correctly redirects to home page")
        else:
            print(f"❌ Registration redirects to {redirect_url}, expected /home/")
    else:
        print(f"❌ Registration failed with status code: {response.status_code}")
    
    # Clean up
    user.delete()
    try:
        User.objects.filter(username='newuser_redirect').delete()
    except:
        pass
    
    print("\n🎉 Login Redirect Test Complete!")

if __name__ == '__main__':
    test_login_redirect() 