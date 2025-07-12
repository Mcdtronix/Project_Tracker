#!/usr/bin/env python
"""
Verification script to check authentication system setup
"""
import os
import sys
import django
from django.conf import settings
from django.urls import reverse, NoReverseMatch

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_tracker.settings')
django.setup()

def verify_auth_setup():
    """Verify all authentication components are properly set up"""
    print("🔍 Verifying Authentication System Setup...")
    
    # Check 1: Settings configuration
    print("\n1. Checking Settings Configuration...")
    try:
        if 'users' in settings.INSTALLED_APPS:
            print("✅ 'users' app is in INSTALLED_APPS")
        else:
            print("❌ 'users' app is NOT in INSTALLED_APPS")
            return False
        
        if settings.LOGIN_URL == '/users/login/':
            print("✅ LOGIN_URL is correctly configured")
        else:
            print(f"❌ LOGIN_URL is incorrect: {settings.LOGIN_URL}")
            return False
        
        if settings.LOGIN_REDIRECT_URL == '/dashboard/':
            print("✅ LOGIN_REDIRECT_URL is correctly configured")
        else:
            print(f"❌ LOGIN_REDIRECT_URL is incorrect: {settings.LOGIN_REDIRECT_URL}")
            return False
        
        if 'django.contrib.auth' in settings.INSTALLED_APPS:
            print("✅ Django auth is in INSTALLED_APPS")
        else:
            print("❌ Django auth is NOT in INSTALLED_APPS")
            return False
        
        if 'django.contrib.sessions' in settings.INSTALLED_APPS:
            print("✅ Django sessions is in INSTALLED_APPS")
        else:
            print("❌ Django sessions is NOT in INSTALLED_APPS")
            return False
        
        if 'django.contrib.messages' in settings.INSTALLED_APPS:
            print("✅ Django messages is in INSTALLED_APPS")
        else:
            print("❌ Django messages is NOT in INSTALLED_APPS")
            return False
        
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False
    
    # Check 2: URL patterns
    print("\n2. Checking URL Patterns...")
    try:
        from project_tracker.urls import urlpatterns
        from users.urls import urlpatterns as user_urlpatterns
        
        # Check main URL patterns
        auth_urls = [url for url in urlpatterns if 'users/' in str(url.pattern)]
        if auth_urls:
            print("✅ Authentication URLs are included in main URLconf")
        else:
            print("❌ Authentication URLs are NOT included in main URLconf")
            return False
        
        # Check user URL patterns
        expected_user_urls = ['register', 'login', 'logout', 'profile', 'change-password']
        user_url_names = [str(url.pattern) for url in user_urlpatterns]
        
        for expected_url in expected_user_urls:
            if any(expected_url in url for url in user_url_names):
                print(f"✅ {expected_url} URL pattern found")
            else:
                print(f"❌ {expected_url} URL pattern NOT found")
                return False
        
    except Exception as e:
        print(f"❌ Error checking URL patterns: {e}")
        return False
    
    # Check 3: Views
    print("\n3. Checking Views...")
    try:
        from users.views import register, CustomLoginView, CustomLogoutView, profile, change_password
        
        print("✅ register view imported successfully")
        print("✅ CustomLoginView imported successfully")
        print("✅ CustomLogoutView imported successfully")
        print("✅ profile view imported successfully")
        print("✅ change_password view imported successfully")
        
    except ImportError as e:
        print(f"❌ Error importing views: {e}")
        return False
    
    # Check 4: Forms
    print("\n4. Checking Forms...")
    try:
        from users.forms import CustomUserCreationForm, CustomAuthenticationForm
        
        print("✅ CustomUserCreationForm imported successfully")
        print("✅ CustomAuthenticationForm imported successfully")
        
    except ImportError as e:
        print(f"❌ Error importing forms: {e}")
        return False
    
    # Check 5: Templates
    print("\n5. Checking Templates...")
    template_files = [
        'registration/login.html',
        'registration/register.html',
        'registration/profile.html',
        'registration/change_password.html',
        'base.html',
        'landing.html'
    ]
    
    for template in template_files:
        template_path = os.path.join(settings.BASE_DIR, 'templates', template)
        if os.path.exists(template_path):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} does NOT exist")
            return False
    
    # Check 6: Database models
    print("\n6. Checking Database Models...")
    try:
        from django.contrib.auth.models import User
        from django.db import connection
        
        # Check if User model is accessible
        user_count = User.objects.count()
        print(f"✅ User model is accessible (current users: {user_count})")
        
        # Check if database is working
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
            if cursor.fetchone():
                print("✅ auth_user table exists")
            else:
                print("❌ auth_user table does NOT exist")
                return False
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    
    # Check 7: Middleware
    print("\n7. Checking Middleware...")
    required_middleware = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ]
    
    for middleware in required_middleware:
        if middleware in settings.MIDDLEWARE:
            print(f"✅ {middleware} is in MIDDLEWARE")
        else:
            print(f"❌ {middleware} is NOT in MIDDLEWARE")
            return False
    
    print("\n🎉 Authentication System Setup Verification Complete!")
    print("✅ All components are properly configured and ready to use.")
    
    return True

def check_url_resolution():
    """Check if all URLs can be resolved"""
    print("\n🔗 Checking URL Resolution...")
    
    urls_to_check = [
        ('users:register', 'Registration URL'),
        ('users:login', 'Login URL'),
        ('users:logout', 'Logout URL'),
        ('users:profile', 'Profile URL'),
        ('users:change_password', 'Change Password URL'),
        ('landing', 'Landing Page URL'),
        ('dashboard', 'Dashboard URL'),
    ]
    
    for url_name, description in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except NoReverseMatch as e:
            print(f"❌ {description}: {e}")
            return False
    
    print("✅ All URLs can be resolved successfully!")
    return True

if __name__ == '__main__':
    print("🚀 Starting Authentication System Verification...")
    
    # Verify setup
    setup_ok = verify_auth_setup()
    
    if setup_ok:
        # Check URL resolution
        urls_ok = check_url_resolution()
        
        if urls_ok:
            print("\n🎯 All verifications passed! Authentication system is ready.")
            print("\n📝 You can now:")
            print("1. Run: python manage.py migrate")
            print("2. Run: python manage.py runserver")
            print("3. Visit: http://localhost:8000")
            print("4. Test registration and login functionality")
        else:
            print("\n❌ URL resolution failed. Please check URL patterns.")
    else:
        print("\n❌ Setup verification failed. Please fix the issues above.") 