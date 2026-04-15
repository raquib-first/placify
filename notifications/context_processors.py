from .models import Notification

def notification_data(request):
    if request.user.is_authenticated:

        # ✅ Full queryset
        all_notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        # ✅ Count from full queryset
        unread_count = all_notifications.filter(is_read=False).count()

        # ✅ Slice AFTER everything
        notifications = all_notifications[:5]

        return {
            "notifications": notifications,
            "unread_count": unread_count
        }

    return {}