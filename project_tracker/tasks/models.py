# tasks/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from projects.models import Project

class Task(models.Model):
    """
    Comprehensive Task Model
    """
    class Status(models.TextChoices):
        TODO = 'TODO', _('To Do')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        REVIEW = 'REVIEW', _('Under Review')
        COMPLETED = 'COMPLETED', _('Completed')
        BLOCKED = 'BLOCKED', _('Blocked')

    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Relationships
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )

    # Task Metadata
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.TODO
    )
    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )

    # Temporal Fields
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)

    # Time Tracking
    estimated_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    actual_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_overdue(self):
        """
        Check if task is overdue
        """
        from django.utils import timezone
        return (self.due_date and 
                self.due_date < timezone.now().date() and 
                self.status != self.Status.COMPLETED)

    class Meta:
        ordering = ['-created_at']

