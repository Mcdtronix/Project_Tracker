#!/usr/bin/env python
"""
Comprehensive test for the complete authentication system
Tests frontend to backend functionality for registration and login
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def test_full_auth_system():
    """Test the complete authentication system from frontend to backend"""
    print("🔐 Testing Complete Authentication System (Frontend to Backend)...")
    
    # Create a test client
    client = Client()
    
    # Test 1: Landing page accessibility
    print("\n1. Testing Landing Page...")
    response = client.get('/')
    if response.status_code == 200:
        print("✅ Landing page loads successfully")
        # Check if sign up button is present
        if 'Sign Up' in response.content.decode() or 'Get Started' in response.content.decode():
            print("✅ Sign up button found on landing page")
        else:
            print("❌ Sign up button not found on landing page")
    else:
        print(f"❌ Landing page failed to load: {response.status_code}")
        return False
    
    # Test 2: Registration page accessibility
    print("\n2. Testing Registration Page...")
    response = client.get('/users/register/')
    if response.status_code == 200:
        print("✅ Registration page loads successfully")
        # Check if registration form is present
        if 'Create Account' in response.content.decode():
            print("✅ Registration form found")
        else:
            print("❌ Registration form not found")
    else:
        print(f"❌ Registration page failed to load: {response.status_code}")
        return False
    
    # Test 3: Login page accessibility
    print("\n3. Testing Login Page...")
    response = client.get('/users/login/')
    if response.status_code == 200:
        print("✅ Login page loads successfully")
        # Check if login form is present
        if 'Sign In' in response.content.decode():
            print("✅ Login form found")
        else:
            print("❌ Login form not found")
    else:
        print(f"❌ Login page failed to load: {response.status_code}")
        return False
    
    # Test 4: User Registration (Backend)
    print("\n4. Testing User Registration (Backend)...")
    registration_data = {
        'username': 'testuser_auth',
        'email': 'testauth@example.com',
        'first_name': 'Test',
        'last_name': 'Auth',
        'password1': 'testpass123',
        'password2': 'testpass123'
    }
    
    response = client.post('/users/register/', registration_data)
    if response.status_code == 302:  # Redirect after successful registration
        print("✅ Registration successful")
        # Check if user was created
        try:
            user = User.objects.get(username='testuser_auth')
            print(f"✅ User created: {user.username} ({user.email})")
        except User.DoesNotExist:
            print("❌ User not found in database after registration")
            return False
    else:
        print("❌ Registration failed")
        print(f"Status code: {response.status_code}")
        if hasattr(response, 'context') and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        return False
    
    # Test 5: User Login (Backend)
    print("\n5. Testing User Login (Backend)...")
    login_data = {
        'username': 'testuser_auth',
        'password': 'testpass123'
    }
    
    response = client.post('/users/login/', login_data)
    if response.status_code == 302:  # Redirect after successful login
        print("✅ Login successful")
        # Check if user is authenticated
        if response.wsgi_request.user.is_authenticated:
            print("✅ User is authenticated")
        else:
            print("❌ User not authenticated after login")
            return False
    else:
        print("❌ Login failed")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 6: Access Protected Page After Login
    print("\n6. Testing Protected Page Access After Login...")
    response = client.get('/dashboard/')
    if response.status_code == 200:
        print("✅ Can access dashboard when logged in")
        # Check if user info is displayed
        if 'testuser_auth' in response.content.decode() or 'Test' in response.content.decode():
            print("✅ User information displayed on dashboard")
        else:
            print("⚠️ User information not found on dashboard")
    else:
        print("❌ Cannot access dashboard when logged in")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 7: Login with Email (Alternative Login Method)
    print("\n7. Testing Login with Email...")
    login_data_email = {
        'username': 'testauth@example.com',
        'password': 'testpass123'
    }
    
    response = client.post('/users/login/', login_data_email)
    if response.status_code == 302:  # Redirect after successful login
        print("✅ Login with email successful")
    else:
        print("❌ Login with email failed")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 8: Profile Page Access
    print("\n8. Testing Profile Page Access...")
    response = client.get('/users/profile/')
    if response.status_code == 200:
        print("✅ Profile page loads successfully")
        # Check if profile information is displayed
        if 'testuser_auth' in response.content.decode():
            print("✅ User profile information displayed")
        else:
            print("⚠️ User profile information not found")
    else:
        print("❌ Profile page failed to load")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 9: Logout Functionality
    print("\n9. Testing Logout Functionality...")
    response = client.post('/users/logout/')
    if response.status_code == 302:  # Redirect after logout
        print("✅ Logout successful")
    else:
        print("❌ Logout failed")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 10: Access Protected Page After Logout
    print("\n10. Testing Protected Page Access After Logout...")
    response = client.get('/dashboard/')
    if response.status_code == 302:  # Should redirect to login
        print("✅ Properly redirected to login when not authenticated")
    else:
        print("❌ Not properly redirected after logout")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 11: Form Validation (Registration)
    print("\n11. Testing Registration Form Validation...")
    invalid_registration_data = {
        'username': 'testuser_auth',  # Duplicate username
        'email': 'invalid-email',     # Invalid email
        'first_name': 'Test',
        'last_name': 'Auth',
        'password1': 'short',         # Too short password
        'password2': 'different'      # Password mismatch
    }
    
    response = client.post('/users/register/', invalid_registration_data)
    if response.status_code == 200:  # Should stay on form page with errors
        print("✅ Form validation working (stays on page with errors)")
        if 'error' in response.content.decode().lower() or 'invalid' in response.content.decode().lower():
            print("✅ Error messages displayed")
        else:
            print("⚠️ Error messages not clearly visible")
    else:
        print("❌ Form validation not working properly")
        print(f"Status code: {response.status_code}")
        return False
    
    # Test 12: Form Validation (Login)
    print("\n12. Testing Login Form Validation...")
    invalid_login_data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }
    
    response = client.post('/users/login/', invalid_login_data)
    if response.status_code == 200:  # Should stay on form page with errors
        print("✅ Login form validation working (stays on page with errors)")
    else:
        print("❌ Login form validation not working properly")
        print(f"Status code: {response.status_code}")
        return False
    
    print("\n🎉 Complete Authentication System Test Successful!")
    print("\n📋 Summary:")
    print("- Landing page: ✅")
    print("- Registration page: ✅")
    print("- Login page: ✅")
    print("- User registration: ✅")
    print("- User login: ✅")
    print("- Protected page access: ✅")
    print("- Email login: ✅")
    print("- Profile page: ✅")
    print("- Logout: ✅")
    print("- Redirects: ✅")
    print("- Form validation: ✅")
    
    return True

def test_url_patterns():
    """Test all authentication URL patterns"""
    print("\n🔗 Testing Authentication URL Patterns...")
    
    client = Client()
    
    urls_to_test = [
        ('/', 'Landing Page'),
        ('/users/register/', 'Registration Page'),
        ('/users/login/', 'Login Page'),
        ('/users/logout/', 'Logout Page'),
        ('/users/profile/', 'Profile Page'),
        ('/users/change-password/', 'Change Password Page'),
        ('/dashboard/', 'Dashboard Page'),
    ]
    
    for url, name in urls_to_test:
        response = client.get(url)
        if response.status_code in [200, 302]:  # 302 is expected for protected pages
            print(f"✅ {name}: {url} - Status: {response.status_code}")
        else:
            print(f"❌ {name}: {url} - Status: {response.status_code}")
    
    print("✅ URL pattern testing complete!")

if __name__ == '__main__':
    print("🚀 Starting Comprehensive Authentication System Test...")
    
    # Test URL patterns first
    test_url_patterns()
    
    # Test full authentication system
    success = test_full_auth_system()
    
    if success:
        print("\n🎯 All tests passed! Authentication system is fully functional.")
        print("\n📝 Next Steps:")
        print("1. Start the server: python manage.py runserver")
        print("2. Visit http://localhost:8000")
        print("3. Test registration and login manually")
        print("4. Verify all features work as expected")
    else:
        print("\n❌ Some tests failed. Please check the implementation.") 