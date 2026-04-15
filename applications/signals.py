from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication, Notification

@receiver(post_save, sender=JobApplication)
def application_status_notification(sender, instance, created, **kwargs):
    if not created:  # Only trigger on update
        student_user = instance.student.user  # StudentProfile → User
        Notification.objects.create(
            recipient=student_user,
            message=f"Your application for '{instance.job.title}' has been {instance.status}."
        )
