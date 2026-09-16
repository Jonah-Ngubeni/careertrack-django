from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobApplicationForm, SignUpForm
from .models import JobApplication


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "applications/home.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    applications = JobApplication.objects.filter(user=request.user)

    context = {
        "total_applications": applications.count(),
        "saved_count": applications.filter(
            status=JobApplication.Status.SAVED
        ).count(),
        "applied_count": applications.filter(
            status=JobApplication.Status.APPLIED
        ).count(),
        "interview_count": applications.filter(
            status=JobApplication.Status.INTERVIEW
        ).count(),
        "offer_count": applications.filter(
            status=JobApplication.Status.OFFER
        ).count(),
        "recent_applications": applications[:5],
    }

    return render(request, "applications/dashboard.html", context)


@login_required
def application_list(request):
    applications = JobApplication.objects.filter(user=request.user)
    search_query = request.GET.get("search", "").strip()
    selected_status = request.GET.get("status", "").strip()

    if search_query:
        applications = applications.filter(
            Q(company__icontains=search_query)
            | Q(position__icontains=search_query)
            | Q(location__icontains=search_query)
        )

    if selected_status:
        applications = applications.filter(status=selected_status)

    context = {
        "applications": applications,
        "search_query": search_query,
        "selected_status": selected_status,
        "status_choices": JobApplication.Status.choices,
    }

    return render(request, "applications/application_list.html", context)


@login_required
def application_detail(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "applications/application_detail.html",
        {"application": application},
    )


@login_required
def application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, "Job application added successfully.")
            return redirect("application_detail", pk=application.pk)
    else:
        form = JobApplicationForm()

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
            "page_title": "Add application",
            "button_text": "Save application",
        },
    )


@login_required
def application_update(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=application)

        if form.is_valid():
            form.save()
            messages.success(request, "Job application updated successfully.")
            return redirect("application_detail", pk=application.pk)
    else:
        form = JobApplicationForm(instance=application)

    return render(
        request,
        "applications/application_form.html",
        {
            "form": form,
            "page_title": "Edit application",
            "button_text": "Update application",
        },
    )


@login_required
def application_delete(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        application.delete()
        messages.success(request, "Job application deleted.")
        return redirect("application_list")

    return render(
        request,
        "applications/application_confirm_delete.html",
        {"application": application},
    )