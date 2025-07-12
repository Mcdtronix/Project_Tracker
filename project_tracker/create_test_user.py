#!/usr/bin/env python
"""
Create a test user for login testing
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create a test user for login testing"""
    print("🔧 Creating test user...")
    
    # Check if test user already exists
    if User.objects.filter(username='testuser').exists():
        print("✅ Test user 'testuser' already exists")
        user = User.objects.get(username='testuser')
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.first_name} {user.last_name}")
        return
    
    # Create test user
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123',
        first_name='Test',
        last_name='User'
    )
    
    print("✅ Test user created successfully!")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Password: TestPass123")
    print(f"   Name: {user.first_name} {user.last_name}")
    print("\n🎯 You can now test login with:")
    print("   Username: testuser")
    print("   Password: TestPass123")
    print("   Or Email: test@example.com")
    print("   Password: TestPass123")

if __name__ == '__main__':
    create_test_user() 