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

    def clean(self):
        cleaned_data = super().clean()
        date_applied = cleaned_data.get("date_applied")
        closing_date = cleaned_data.get("closing_date")

        if date_applied and closing_date and closing_date < date_applied:
            self.add_error(
                "closing_date",
                "Closing date cannot be earlier than the application date.",
            )

        return cleaned_data