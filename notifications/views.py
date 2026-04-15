from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def fetch_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    data = []
    for n in notifications:
        data.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%d %b %Y %H:%M"),
        })

    unread_count = notifications.filter(is_read=False).count()

    return JsonResponse({
        "notifications": data,
        "unread_count": unread_count
    })


@login_required
def mark_as_read(request, notif_id):
    Notification.objects.filter(
        id=notif_id,
        user=request.user
    ).update(is_read=True)

    return JsonResponse({"success": True})
