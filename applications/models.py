"""Database models for storing users' job applications."""

from datetime import date

from django.conf import settings
from django.db import models


class JobApplication(models.Model):
    """Represent a job application belonging to an authenticated user."""

    class Status(models.TextChoices):
        """Provide the available stages of a job application."""

        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    company = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SAVED,
    )
    date_applied = models.DateField(default=date.today)
    closing_date = models.DateField(blank=True, null=True)
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_applied", "-created_at"]

    def __str__(self):
        """Return a readable description of the job application."""
        return f"{self.position} at {self.company}"
