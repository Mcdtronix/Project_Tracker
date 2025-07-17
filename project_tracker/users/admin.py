from django.contrib import admin
from .models import UserSettings
from .models import UserNotification

# Register your models here.
admin.site.register(UserSettings)
admin.site.register(UserNotification)
