# Authentication System Testing Guide

## Overview
This guide provides comprehensive instructions for testing and verifying that the authentication system is fully functional from frontend to backend.

## 🚀 Quick Start

### 1. Run Verification Script
```bash
cd project_tracker
python verify_auth_setup.py
```

### 2. Run Comprehensive Tests
```bash
python test_full_auth_system.py
```

### 3. Start the Server
```bash
python manage.py migrate
python manage.py runserver
```

### 4. Test Manually
Visit `http://localhost:8000` and test the registration/login flow.

## 🔍 Verification Steps

### Step 1: System Setup Verification
The `verify_auth_setup.py` script checks:

#### ✅ Settings Configuration
- `users` app in `INSTALLED_APPS`
- `LOGIN_URL` set to `/users/login/`
- `LOGIN_REDIRECT_URL` set to `/dashboard/`
- Required Django apps (auth, sessions, messages)

#### ✅ URL Patterns
- Authentication URLs included in main URLconf
- All user URLs present (register, login, logout, profile, change-password)

#### ✅ Views and Forms
- All authentication views imported successfully
- Custom forms imported successfully

#### ✅ Templates
- All authentication templates exist
- Base template and landing page exist

#### ✅ Database
- User model accessible
- auth_user table exists

#### ✅ Middleware
- Session middleware
- Authentication middleware
- Messages middleware
- CSRF middleware

### Step 2: Functional Testing
The `test_full_auth_system.py` script tests:

#### ✅ Frontend Accessibility
- Landing page loads with sign-up button
- Registration page loads with form
- Login page loads with form

#### ✅ Backend Functionality
- User registration creates account
- User login authenticates properly
- Protected pages accessible when logged in
- Logout terminates session

#### ✅ Alternative Login Methods
- Login with email address
- Login with username

#### ✅ Form Validation
- Registration form validation
- Login form validation
- Error message display

#### ✅ Security Features
- CSRF protection
- Password validation
- Session management
- Proper redirects

## 🧪 Manual Testing Checklist

### Registration Flow
1. **Visit Landing Page**
   - Go to `http://localhost:8000`
   - Verify "Get Started" button is present
   - Click "Get Started" or "Sign Up"

2. **Fill Registration Form**
   - Enter first name and last name
   - Choose unique username
   - Enter valid email address
   - Create password (minimum 8 characters)
   - Confirm password
   - Click "Create Account"

3. **Verify Registration**
   - Should redirect to dashboard
   - Welcome message should appear
   - User should be logged in automatically

### Login Flow
1. **Access Login Page**
   - Go to `http://localhost:8000/users/login/`
   - Or click "Sign In" from navbar

2. **Login with Username**
   - Enter username
   - Enter password
   - Click "Sign In"

3. **Login with Email**
   - Enter email address
   - Enter password
   - Click "Sign In"

4. **Verify Login**
   - Should redirect to dashboard
   - User dropdown should show in navbar
   - Protected pages should be accessible

### Profile Management
1. **Access Profile**
   - Click user dropdown in navbar
   - Select "My Profile"

2. **View Profile Information**
   - Verify account details are displayed
   - Check project and task statistics
   - Verify account actions are available

3. **Change Password**
   - Click "Change Password" button
   - Enter current password
   - Enter new password
   - Confirm new password
   - Click "Update Password"

### Logout Flow
1. **Logout from Navbar**
   - Click user dropdown
   - Click "Sign Out"
   - Should redirect to landing page

2. **Logout from Profile**
   - Go to profile page
   - Click "Sign Out" button
   - Should redirect to landing page

3. **Verify Logout**
   - Should not be able to access protected pages
   - Should redirect to login page
   - Navbar should show "Sign In" and "Sign Up" buttons

## 🔧 Troubleshooting

### Common Issues

#### 1. "No module named 'users'"
**Solution**: Ensure `users` app is in `INSTALLED_APPS` in settings.py

#### 2. "URL not found" errors
**Solution**: Check that authentication URLs are included in main URLconf

#### 3. "Template does not exist" errors
**Solution**: Verify all template files exist in the correct locations

#### 4. "Database table does not exist"
**Solution**: Run `python manage.py migrate`

#### 5. "CSRF verification failed"
**Solution**: Ensure CSRF middleware is enabled and forms include CSRF tokens

#### 6. "Login redirect loop"
**Solution**: Check `LOGIN_URL` and `LOGIN_REDIRECT_URL` settings

### Debug Steps

1. **Check Django Logs**
   ```bash
   python manage.py runserver --verbosity=2
   ```

2. **Verify Database**
   ```bash
   python manage.py dbshell
   .tables
   SELECT * FROM auth_user;
   ```

3. **Test URL Resolution**
   ```python
   python manage.py shell
   from django.urls import reverse
   reverse('users:login')
   ```

4. **Check Template Context**
   Add debug prints in views or use Django Debug Toolbar

## 📋 Expected Behavior

### Successful Registration
- Form submits without errors
- User account created in database
- Automatic login after registration
- Redirect to dashboard
- Success message displayed

### Successful Login
- Form submits without errors
- User authenticated
- Redirect to dashboard
- User dropdown appears in navbar
- Protected pages accessible

### Failed Registration/Login
- Form stays on page
- Error messages displayed
- No redirect occurs
- User not authenticated

### Logout
- Session terminated
- Redirect to landing page
- Success message displayed
- Protected pages no longer accessible

## 🎯 Success Criteria

The authentication system is fully functional when:

✅ **All verification scripts pass**
✅ **Manual testing works for all flows**
✅ **No error messages in console**
✅ **All URLs resolve correctly**
✅ **Forms validate properly**
✅ **Security features work**
✅ **User experience is smooth**

## 📞 Support

If you encounter issues:

1. **Run verification scripts** to identify problems
2. **Check Django logs** for error details
3. **Verify database migrations** are applied
4. **Test URL patterns** manually
5. **Review template syntax** for errors

The authentication system is designed to be robust and user-friendly, with comprehensive error handling and validation. 