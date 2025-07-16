from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register(request):
    """
    User registration view with enhanced validation
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Log the user in after successful registration
                login(request, user)
                messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'An error occurred during registration. Please try again.')
                # Log the error for debugging
                print(f"Registration error: {e}")
        else:
            # Enhanced error handling
            error_count = len(form.errors)
            if error_count == 1:
                messages.error(request, 'Please correct the error below.')
            else:
                messages.error(request, f'Please correct the {error_count} errors below.')
            
            # Log validation errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Validation error in {field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    """
    Custom login view with enhanced styling and validation
    """
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def dispatch(self, request, *args, **kwargs):
        print(f"[LOGIN DEBUG] Request method: {request.method}, User authenticated: {request.user.is_authenticated}")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(f"[LOGIN DEBUG] POST data: {request.POST}")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print(f"[LOGIN DEBUG] Form is valid. User: {form.get_user()}")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"[LOGIN DEBUG] Form is invalid. Errors: {form.errors}")
        # Enhanced error handling
        error_count = len(form.errors)
        if error_count == 1:
            messages.error(self.request, 'Please correct the error below.')
        else:
            messages.error(self.request, f'Please correct the {error_count} errors below.')
        
        # Log validation errors for debugging
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Login validation error in {field}: {error}")
        
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    """
    Custom logout view
    """
    next_page = 'landing'
    http_method_names = ['get', 'post']  # Allow both GET and POST
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye {request.user.first_name}! You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request):
    """
    User profile view
    """
    from projects.models import Project
    from tasks.models import Task
    
    # Get user's projects and tasks
    user_projects = Project.objects.filter(team_members=request.user)
    user_tasks = Task.objects.filter(project__team_members=request.user)
    
    # Calculate statistics
    total_projects = user_projects.count()
    active_projects = user_projects.filter(status='IN_PROGRESS').count()
    completed_projects = user_projects.filter(status='COMPLETED').count()
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='COMPLETED').count()
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    
    return render(request, 'registration/profile.html', context)

@login_required
def change_password(request):
    """
    Change password view
    """
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            user.set_password(new_password1)
            user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    
    return render(request, 'registration/change_password.html')

def login_debug(request):
    """
    Debug login view to test frontend-backend interaction
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        print("DEBUG: POST request received")
        print(f"DEBUG: POST data: {request.POST}")
        
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            print("DEBUG: Form is valid")
            user = form.get_user()
            if user:
                print(f"DEBUG: User found: {user.username}")
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                print("DEBUG: User not found")
                messages.error(request, 'Invalid credentials.')
        else:
            print(f"DEBUG: Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login_debug.html', {'form': form})
