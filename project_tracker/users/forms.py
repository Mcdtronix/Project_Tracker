from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with enhanced styling and comprehensive validation
    """
    # Custom validators
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message='Username can only contain letters, numbers, and underscores.'
    )
    
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message='Name can only contain letters and spaces.'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'pattern': r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
            'title': 'Please enter a valid email address'
        }),
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'pattern': r'[A-Za-z\s]+',
            'title': 'Name can only contain letters and spaces'
        }),
        error_messages={
            'required': 'First name is required.',
            'max_length': 'First name cannot exceed 30 characters.',
        }
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'pattern': r'[A-Za-z\s]+',
            'title': 'Name can only contain letters and spaces'
        }),
        error_messages={
            'required': 'Last name is required.',
            'max_length': 'Last name cannot exceed 30 characters.',
        }
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize username field
        self.fields['username'] = forms.CharField(
            max_length=150,
            required=True,
            validators=[self.__class__.username_validator],
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username (letters, numbers, underscores only)',
                'pattern': '[a-zA-Z0-9_]+',
                'title': 'Username can only contain letters, numbers, and underscores'
            }),
            error_messages={
                'required': 'Username is required.',
                'max_length': 'Username cannot exceed 150 characters.',
            }
        )
        
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password (minimum 8 characters)',
            'minlength': '8',
            'pattern': r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
            'title': 'Password must contain at least 8 characters, including uppercase, lowercase, and numbers'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'minlength': '8'
        })
        
        # Enhanced help text
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, numbers, and underscores only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters, including uppercase, lowercase, and numbers.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose a different one.')
        
        # Additional username validation
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        
        if username.lower() in ['admin', 'root', 'administrator', 'user', 'test']:
            raise ValidationError('This username is not allowed. Please choose a different one.')
        
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use. Please use a different email or try logging in.')
        
        # Additional email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Please enter a valid email address.')
        
        # Check for disposable email domains (basic check)
        disposable_domains = ['10minutemail.com', 'tempmail.org', 'guerrillamail.com']
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            raise ValidationError('Please use a valid email address. Disposable email addresses are not allowed.')
        
        return email
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        # Remove extra spaces and capitalize
        first_name = ' '.join(first_name.split()).title()
        
        if len(first_name) < 2:
            raise ValidationError('First name must be at least 2 characters long.')
        
        return first_name
        
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        # Remove extra spaces and capitalize
        last_name = ' '.join(last_name.split()).title()
        
        if len(last_name) < 2:
            raise ValidationError('Last name must be at least 2 characters long.')
        
        return last_name
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Enhanced password validation
        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        if not re.search(r'[A-Z]', password1):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password1):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        if not re.search(r'\d', password1):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for common passwords
        common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome']
        if password1.lower() in common_passwords:
            raise ValidationError('This password is too common. Please choose a more secure password.')
        
        return password1
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match. Please make sure both passwords are identical.')
        
        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form with enhanced styling and validation
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'username'
        }),
        error_messages={
            'required': 'Username or email is required.',
        }
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        }),
        error_messages={
            'required': 'Password is required.',
        }
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Trim whitespace
        username = username.strip()
        
        if not username:
            raise ValidationError('Username or email is required.')
        
        # Allow login with email or username
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError('No account found with this email address. Please check your email or try registering.')
        
        return username 