# CareerTrack – Job Application Tracker

CareerTrack is a Django web application that helps users organise and monitor their job applications. Users can create an account, securely log in, record job opportunities, update application progress, search and filter records, and view summary statistics from a personal dashboard.

# Table of Contents

- [Features](#features)
- [Application Statuses](#application-statuses)
- [Technologies Used](#technologies-used)
- [Database Model](#database-model)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Automated Tests](#running-the-automated-tests)
- [How to Use CareerTrack](#how-to-use-careertrack)
- [Screenshots](#screenshots)
- [Security](#security)
- [Development Status](#development-status)
- [Future Improvements](#future-improvements)
- [Author](#author)

# Features

- User registration
- Secure login and logout
- Personal dashboard
- Job-application statistics
- Create job applications
- View application details
- Update existing applications
- Delete applications with confirmation
- Search by company, position, or location
- Filter applications by status
- User-specific data protection
- Success messages after creating, updating, or deleting records
- Responsive interface for desktop and mobile devices
- Automated Django tests

# Application Statuses

CareerTrack supports the following application stages:

- Saved
- Applied
- Interview
- Offer
- Rejected

# Technologies Used

- Python 3
- Django 6
- HTML5
- CSS3
- SQLite
- Django authentication
- Django ORM
- Django testing framework
- Git and GitHub

# Database Model

The `JobApplication` model stores:

- User
- Company
- Position
- Location
- Application status
- Date applied
- Closing date
- Job URL
- Notes
- Creation date
- Last updated date

Each job application belongs to a specific authenticated user. Users cannot view or modify another user’s application records.

# Project Structure

```text
job_application_tracker/
├── applications/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── job_tracker/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── screenshots/
│   ├── applications.png
│   ├── dashboard.png
│   └── homepage.png
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── applications/
│   │   ├── application_confirm_delete.html
│   │   ├── application_detail.html
│   │   ├── application_form.html
│   │   ├── application_list.html
│   │   ├── dashboard.html
│   │   └── home.html
│   ├── registration/
│   │   ├── login.html
│   │   └── signup.html
│   └── base.html
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

# Installation

# 1. Clone the repository

```powershell
git clone https://github.com/Jonah-Ngubeni/careertrack-django.git
cd careertrack-django
```

# 2. Create a virtual environment

```powershell
python -m venv venv
```

# 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source venv/bin/activate
```

# 4. Install the dependencies

```powershell
python -m pip install -r requirements.txt
```

# 5. Apply the database migrations

```powershell
python manage.py migrate
```

# 6. Start the development server

```powershell
python manage.py runserver
```

Open the following address in a browser:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

# Running the Automated Tests

Run the complete test suite with:

```powershell
python manage.py test
```

The project currently includes 12 automated tests covering:

- Model string representation
- Authentication protection
- Dashboard access
- Dashboard content
- Creating applications
- Updating applications
- Deleting applications
- Searching applications
- Empty search results
- Status filtering
- Protection against accessing another user’s records
- User-specific application lists

A successful test run should finish with:

```text
Ran 12 tests

OK
```

# How to Use CareerTrack

1. Open the homepage.
2. Select **Create account**.
3. Register a username and password.
4. Log in to access the dashboard.
5. Select **Add application**.
6. Enter the job-application information.
7. Use the dashboard to monitor application totals.
8. Open an application to view, edit, or delete it.
9. Use search and status filters to find specific records.
10. Log out when finished.

# Screenshots

# Home Page

![CareerTrack home page](screenshots/homepage.png)

# Dashboard

![CareerTrack dashboard](screenshots/dashboard.png)

# Applications Page

![CareerTrack applications page](screenshots/applications.png)

# Security

CareerTrack uses Django’s built-in authentication system.

Protected features require the user to log in. Database queries are restricted to the currently authenticated user, preventing users from accessing one another’s job-application records.

Passwords are processed and stored using Django’s secure password-hashing system.

# Development Status

The following functionality has been implemented and tested:

- Authentication
- Database integration
- Complete CRUD functionality
- Dashboard statistics
- Search and filtering
- User-data isolation
- Responsive styling
- Automated testing

# Future Improvements

Potential future improvements include:

- Email reminders for closing dates and interviews
- Document and CV uploads
- Interview scheduling
- Application analytics and charts
- Password-reset functionality
- Pagination
- Deployment to a production hosting platform

# Author

[Jonah Ngubeni] (https://github.com/Jonah-Ngubeni)

Developed as a Django capstone project for the HyperionDev Software Engineering Bootcamp.