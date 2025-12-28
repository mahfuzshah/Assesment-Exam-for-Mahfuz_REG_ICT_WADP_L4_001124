from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ("recruiter", "Recruiter"),
        ("jobseeker", "Jobseeker"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class Job(models.Model):
    CATEGORY_CHOICES = [
        ("tech", "Technology"),
        ("finance", "Finance"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=200)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    number_of_openings = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    skills_required = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("selected", "Selected"),
        ("rejected", "Rejected"),
    ]
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="application_resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("jobseeker", "job")

    def __str__(self):
        return f"{self.jobseeker.username} applied for {self.job.title}"
