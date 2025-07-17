from django.conf import settings
from django.db import models

# Create your models here.

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    # Project settings
    default_project_status = models.CharField(max_length=20, default='IN_PROGRESS')
    default_priority = models.CharField(max_length=20, default='MEDIUM')
    show_completed_tasks = models.BooleanField(default=True)
    enable_templates = models.BooleanField(default=False)
    # System settings
    theme = models.CharField(max_length=20, default='light')
    language = models.CharField(max_length=10, default='en')
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')
    refresh_interval = models.IntegerField(default=60)  # seconds
    items_per_page = models.IntegerField(default=25)
    enable_animations = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"
