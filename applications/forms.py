from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import JobApplication


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = (
            "company",
            "position",
            "location",
            "status",
            "date_applied",
            "closing_date",
            "job_url",
            "notes",
        )
        widgets = {
            "date_applied": forms.DateInput(attrs={"type": "date"}),
            "closing_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Add interview notes, contacts, or reminders.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"