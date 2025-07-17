from django.urls import path
from . import views
from .views import UserSettingsView
from .views import UserQuickStatsView
from .views import UserNotificationListView, mark_notification_read

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login-debug/', views.login_debug, name='login_debug'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]

urlpatterns += [
    path('api/users/settings/', UserSettingsView.as_view(), name='user-settings-api'),
    path('api/users/quick-stats/', UserQuickStatsView.as_view(), name='user-quick-stats-api'),
    path('api/users/notifications/', UserNotificationListView.as_view(), name='user-notifications-api'),
    path('api/users/notifications/<int:pk>/read/', mark_notification_read, name='user-notification-read-api'),
] 