# projects/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class ProjectCategory(models.Model):
    """
    Project categories to help organize and classify projects
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Project Categories"

class Project(models.Model):
    """
    Comprehensive Project Model
    """
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', _('Planning')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        ON_HOLD = 'ON_HOLD', _('On Hold')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Relationships
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Project Metadata
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PLANNING
    )
    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )

    # Temporal Fields
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    estimated_completion_date = models.DateField(null=True, blank=True)

    # Financial Fields
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def calculate_progress(self):
        """
        Calculate project progress based on tasks
        """
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(status='COMPLETED').count()
        return (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    def is_overdue(self):
        """
        Check if project is overdue
        """
        from django.utils import timezone
        return (self.estimated_completion_date and 
                self.estimated_completion_date < timezone.now().date())

    class Meta:
        ordering = ['-created_at']