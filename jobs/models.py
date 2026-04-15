from django.db import models
from profiles.models import CompanyProfile,StudentProfile
from django.utils import timezone

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    ]

    REMOTE_TYPE_CHOICES = [
        ('ONSITE', 'On-site'),
        ('REMOTE', 'Remote'),
        ('HYBRID', 'Hybrid'),
    ]

    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=150)

    job_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default='FULL-TIME'
    )

    remote_type = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    description = models.TextField()

    required_experience = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="e.g. 0-2 years, 3-5 years"
    )

    skills = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Comma separated skills (Python, Django, SQL)"
    )

    qualifications = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    salary = models.CharField(max_length=100, blank=True)

    application_deadline = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_open(self):
        if not self.is_active:
            return False

        if self.application_deadline:
            return self.application_deadline >= timezone.now().date()

        return True

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"


# jobs/models.py
class SavedJob(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'job')
