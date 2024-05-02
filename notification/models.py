from django.db import models
from django.conf import settings
from django.urls import reverse


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications')
    is_read = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    href = models.URLField(default="")
