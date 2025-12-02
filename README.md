# JobBoard

## Project Overview

This project is a full‑featured **Job Portal Web Application** built with Django which connects **employers** and **job seekers**. The app focuses on solid architecture, accessibility, and realistic hiring flows: job posting, applications, profile management, dashboards, and an event‑driven notification system.

---

## 📌 Project Video

**URL:** https://youtu.be/FCSX9nvp53I

---

## What the Project Is

This is a dedicated **job board**. Core user types are **Employers** and **Job Seekers**. Key flows include:

* Employers create, edit, and delete job listings, and view applications for their jobs.
* Job Seekers create profiles, add education and work experience, upload resumes, apply to jobs through a dedicated application page, and withdraw applications.
* A notification system alerts employers when someone applies or withdraws, and alerts job seekers when an employer views their profile for a specific job.
* Jobs are categorized, and users can filter listings by category.

All functionality is implemented with security and clarity in mind: role checks, form validation, and server‑side protections are applied consistently.

---

## Major Features (High Level)

* **Role‑based authentication:** Custom user model with `role` and email‑based login.
* **Job CRUD:** Employers manage jobs with a dedicated dashboard.
* **Application system:** Dedicated application page, resume upload, prevention of duplicate applications, and withdrawal support.
* **Profile management:** Job seekers manage general info, a short headline, multiple education and work experience entries (with validation).
* **Notifications:** Event‑driven notifications (application, withdrawal, job‑specific profile views) implemented via signals and view logic, with duplicate/ spam protections.
* **Job categories & filtering** for discoverability.

---

## File‑by‑File Overview

This section explains the primary files and what they contain. Files are organized within the Django app structure (apps such as `accounts`, `jobs`, `employers`, `job_seekers` plus project settings, media files, static files and templates).

### `accounts/models.py`

* Custom `User` model (inherits `AbstractUser`). Key fields: `email` (unique, used as `USERNAME_FIELD`), `role` (`employer` or `job_seeker`), `address`, `mobile`, and `headline` (short bio). 
* `Notification` model: unified notification model for both roles, stores type, actor, related job/applicant, read state, and timestamp. 

### `jobs/models.py`

* `Job`: stores job metadata (title, company, description, location, category, date_posted, employer relation).
* `JobCategory`: simple category model.
* `JobApplication`: application record linking job and applicant, including resume upload. Unique constraint on `(job, applicant)` prevents duplicate applications.

### `job_seekers/models.py`

* `Education` and `WorkExperience`: linked to job seekers. 

### `jobs/forms.py`, `employers/forms.py` & `job_seekers/forms.py`

* `UserRegisterForm`, `UserLoginForm`, and `JobSeekerProfileForm`.
* `JobForm`.
* `JobApplicationForm`, `EducationForm`, and `WorkExperienceForm`.

### `accounts/views.py`
* Views for user registration, logging in and out, notification list, marking notification as read and deleting notifications are included here.

### `employers/views.py`
* Views for creating, updating and deleting jobs, employer dashboard, viewing applicants and each applicant's profile are included here.

### `job_seekers/views.py`
* Views for applying and withdrawing from a job, creating, updating and deleting education and work experience, viewing jobseeker dashboard & profile are included here.

### `jobs/views.py`
* Views for job listings and job details are included here.

### `jobs/signals.py`

* `post_save` on `JobApplication` to notify employers of new applications.
* `post_delete` on `JobApplication` to notify employers of withdrawals.

### `templates/`, `media` and `static/`

* `base.html` contains navbar, message rendering, and Bootstrap 5 cdns.
* There are separate template folders for each app.
* Static folder holds CSS.
* Media folder stores the resumes uploaded by the jobseekers.

### `urls.py`

* It provides clean routing for jobs, profiles, dashboards, notifications e.t.c.
* Each app has a separate url.py file.

---

## Key Design Decisions & Rationale

Below I summarize design tradeoffs made during the capstone and why they were chosen.

**Custom User & Email Login.** Creating a custom `User` model early simplifies authentication flows (email login) and allows additional profile fields. This aligns with real production systems.

**Database constraints vs UX checks.** Duplicate applications are prevented with a DB uniqueness constraint (defense in depth), while the UI and view logic provide friendly messages to users.

**Notifications as records.** Using a `Notification` model makes it easy to persist and display notifications, add read/delete actions, and later extend to real‑time delivery.

**Job‑specific profile views.** Notifications for profile views are tracked per `(employer, job, applicant)` tuple, which avoids spam and better reflects the hiring context.

---

## How to Run (short)

1. Clone the repo.
2. Create a virtualenv and `pip install -r requirements.txt`.
3. Configure `settings.py` (set `AUTH_USER_MODEL`, `MEDIA_ROOT`, etc.).
4. `python manage.py makemigrations` and `python manage.py migrate`.
5. `python manage.py createsuperuser` (optional).
6. `python manage.py runserver` and open `http://127.0.0.1:8000/`.

---