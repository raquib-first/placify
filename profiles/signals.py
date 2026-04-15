from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import StudentProfile, CompanyProfile

User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == 'STUDENT':
        StudentProfile.objects.create(user=instance)

    elif instance.role == 'COMPANY':
        CompanyProfile.objects.create(user=instance)
