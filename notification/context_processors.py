from django.contrib.auth.decorators import login_required
from .models import Notification


def add_notifications(request):
    if request.user.is_authenticated:
        notifications_query = Notification.objects.filter(user=request.user).order_by('-timestamp')
        has_unread = notifications_query.filter(is_read=False).exists()
        notifications = notifications_query[:5]
        return {
            'notifications': notifications,
            'has_unread': has_unread
        }
    else:
        return {}