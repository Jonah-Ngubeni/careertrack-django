from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import JobApplicationForm
from .models import JobApplication


User = get_user_model()


class JobApplicationTests(TestCase):
    def setUp(self):
        """Create test users and one job application before each test."""
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPassword123!",
        )

        self.application = JobApplication.objects.create(
            user=self.user,
            company="MTN",
            position="Junior Software Developer",
            location="Midrand, Gauteng",
            status="interview",
            date_applied=date(2026, 9, 13),
            notes="Interview scheduled.",
        )

    def login_test_user(self):
        """Log in the main test user."""
        return self.client.login(
            username="testuser",
            password="StrongPassword123!",
        )

    def test_application_string_representation(self):
        """The model should return a readable application name."""
        self.assertEqual(
            str(self.application),
            "Junior Software Developer at MTN",
        )

    def test_dashboard_requires_login(self):
        """Logged-out visitors should be redirected to login."""
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_logged_in_user_can_view_dashboard(self):
        """A logged-in user should be able to open the dashboard."""
        self.login_test_user()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MTN")
        self.assertContains(
            response,
            "Junior Software Developer",
        )

    def test_dashboard_displays_application_overview(self):
        """The dashboard should display its statistics and records."""
        self.login_test_user()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total")
        self.assertContains(response, "Saved")
        self.assertContains(response, "Applied")
        self.assertContains(response, "Interviews")
        self.assertContains(response, "Offers")
        self.assertContains(
            response,
            "Junior Software Developer",
        )
        self.assertContains(response, "MTN")

    def test_user_can_create_application(self):
        """A logged-in user should be able to create an application."""
        self.login_test_user()

        response = self.client.post(
            reverse("application_create"),
            {
                "company": "Microsoft",
                "position": "Graduate Developer",
                "location": "Johannesburg",
                "status": "saved",
                "date_applied": "2026-09-16",
                "closing_date": "",
                "job_url": "https://example.com/job",
                "notes": "Prepare application documents.",
            },
        )

        self.assertEqual(JobApplication.objects.count(), 2)

        new_application = JobApplication.objects.get(
            company="Microsoft",
        )

        self.assertEqual(new_application.user, self.user)
        self.assertEqual(new_application.status, "saved")

        self.assertRedirects(
            response,
            reverse(
                "application_detail",
                args=[new_application.pk],
            ),
        )

    def test_user_can_update_application(self):
        """A user should be able to update their application."""
        self.login_test_user()

        response = self.client.post(
            reverse(
                "application_update",
                args=[self.application.pk],
            ),
            {
                "company": "MTN",
                "position": "Junior Software Developer",
                "location": "Midrand, Gauteng",
                "status": "offer",
                "date_applied": "2026-09-13",
                "closing_date": "",
                "job_url": "",
                "notes": "Offer received.",
            },
        )

        self.application.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.application.status, "offer")
        self.assertEqual(
            self.application.notes,
            "Offer received.",
        )

    def test_user_can_delete_application(self):
        """A user should be able to delete their application."""
        self.login_test_user()

        response = self.client.post(
            reverse(
                "application_delete",
                args=[self.application.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        application_exists = JobApplication.objects.filter(
            pk=self.application.pk
        ).exists()

        self.assertFalse(application_exists)

    def test_search_finds_matching_application(self):
        """Searching by company should return a matching record."""
        self.login_test_user()

        response = self.client.get(
            reverse("application_list"),
            {"search": "MTN"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MTN")
        self.assertContains(
            response,
            "Junior Software Developer",
        )

    def test_search_hides_non_matching_application(self):
        """A search without matches should hide existing records."""
        self.login_test_user()

        response = self.client.get(
            reverse("application_list"),
            {"search": "QWEREWTRTYR"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No applications found")
        self.assertNotContains(response, "MTN")

    def test_status_filter_returns_matching_application(self):
        """Filtering by status should return matching records."""
        self.login_test_user()

        response = self.client.get(
            reverse("application_list"),
            {"status": "interview"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MTN")
        self.assertContains(response, "Interview")

    def test_user_cannot_view_another_users_application(self):
        """Users must not be able to view another user's record."""
        other_application = JobApplication.objects.create(
            user=self.other_user,
            company="Private Company",
            position="Private Position",
            location="Pretoria",
            status="saved",
            date_applied=date(2026, 9, 16),
        )

        self.login_test_user()

        response = self.client.get(
            reverse(
                "application_detail",
                args=[other_application.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_application_list_only_shows_current_user_records(self):
        """The application list must only show the current user's data."""
        JobApplication.objects.create(
            user=self.other_user,
            company="Hidden Company",
            position="Hidden Position",
            location="Pretoria",
            status="saved",
            date_applied=date(2026, 9, 16),
        )

        self.login_test_user()

        response = self.client.get(reverse("application_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MTN")
        self.assertNotContains(response, "Hidden Company")


class JobApplicationFormValidationTests(TestCase):
    def get_valid_data(self):
        """Return valid form data for closing-date tests."""
        return {
            "company": "Example Company",
            "position": "Software Developer",
            "location": "Johannesburg",
            "status": "applied",
            "date_applied": "2026-09-10",
            "closing_date": "2026-09-30",
            "job_url": "",
            "notes": "",
        }

    def test_rejects_closing_date_before_application_date(self):
        """A closing date before the application date should be rejected."""
        data = self.get_valid_data()
        data["closing_date"] = "2026-09-01"

        form = JobApplicationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("closing_date", form.errors)
        self.assertIn(
            "Closing date cannot be earlier than the application date.",
            form.errors["closing_date"],
        )

    def test_accepts_closing_date_after_application_date(self):
        """A closing date after the application date should be accepted."""
        form = JobApplicationForm(data=self.get_valid_data())

        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_accepts_empty_closing_date(self):
        """The closing date should remain optional."""
        data = self.get_valid_data()
        data["closing_date"] = ""

        form = JobApplicationForm(data=data)

        self.assertTrue(form.is_valid(), form.errors.as_text())