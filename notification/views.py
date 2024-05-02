from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# noinspection PyArgumentList
def send_notification(user, message, url, balance, sign):
    notification = Notification(
        user=user,
        message=message,
        is_read=False,
        href=url
    )
    notification.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "text": {
                "message": message,
                "url": url,
                "balance": balance,
                "sign": sign
            }
        }
    )


@csrf_exempt
def mark_notifications_as_read(request):
    if request.user.is_authenticated and request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


