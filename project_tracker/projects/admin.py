from django.contrib import admin
from .models import  ProjectCategory, Project

# Register your models here.
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name','description')
    search_fields = ('name', 'description')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority','status', 'start_date','end_date', 'estimated_completion_date')
    list_filter = ('name','priority','status','start_date','end_date', 'estimated_completion_date')
    search_fields = ('name', 'priority', 'status')







admin.site.register(ProjectCategory, ProjectCategoryAdmin),
admin.site.register(Project, ProjectAdmin),


