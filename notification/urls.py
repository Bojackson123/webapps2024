from django.urls import path
from .views import mark_notifications_as_read

urlpatterns = [
    path('notifications/mark-as-read/', mark_notifications_as_read, name='mark-notifications-as-read'),
]