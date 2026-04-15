from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Contact & Location
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Education
    university = models.CharField(max_length=150, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Professional Profile
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    # Skills & Links
    skills = models.TextField(
        blank=True,
        help_text="Comma separated skills (Python, Django, SQL)"
    )

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    # Resume
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )
    # 🔒 Privacy Settings
    is_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)

    PROJECT_VISIBILITY_CHOICES = [
        ('all', 'Everyone'),
        ('recruiters', 'Only Recruiters'),
        ('private', 'Only Me'),
    ]

    project_visibility = models.CharField(
        max_length=20,
        choices=PROJECT_VISIBILITY_CHOICES,
        default='all'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"StudentProfile ({self.user})"

    def completion_percentage(self):
        fields = [
            self.phone,
            self.location,
            self.university,
            self.degree,
            self.branch,
            self.graduation_year,
            self.skills,
            self.bio,
            self.resume,
        ]
        filled = sum(1 for field in fields if field)
        return int((filled / len(fields)) * 100)


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 1-10, 11-50, 51-200"
    )
    founded_year = models.IntegerField(null=True, blank=True)

    headquarters = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)

    hr_name = models.CharField(max_length=100, blank=True)
    hr_email = models.EmailField(blank=True)

    linkedin_page = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    is_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)

    def __str__(self):
        return f"CompanyProfile ({self.user})"

    def completion_percentage(self):
        fields = [
            self.company_name,
            self.website,
            self.industry,
            self.company_size,
            self.headquarters,
            self.hr_email,
            self.description,
        ]
        filled = sum(1 for field in fields if field)
        return int((filled / len(fields)) * 100)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, blank=True)
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"