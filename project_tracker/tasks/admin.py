from django.contrib import admin
from . models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'start_date', 'due_date', 'completed_date')
    list_filter = ('title','project', 'priority', 'status', 'start_date', 'due_date', 'completed_date')
    search_fields = ('name', 'project', 'priority', 'status',)


admin.site.register(Task,TaskAdmin)