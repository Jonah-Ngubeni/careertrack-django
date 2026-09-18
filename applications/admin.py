from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Configure job applications in the Django administration site."""

    list_display = (
        "company",
        "position",
        "status",
        "user",
        "date_applied",
    )
    list_filter = (
        "status",
        "date_applied",
    )
    search_fields = (
        "company",
        "position",
        "location",
        "user__username",
    )
    ordering = (
        "-date_applied",
        "-created_at",
    )
    date_hierarchy = "date_applied"