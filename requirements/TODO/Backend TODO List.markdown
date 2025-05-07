# Backend TODO List (Django)

## Setup Environment
- [x] Install Python 3.10+ and verify with `python --version`.
- [x] Install PostgreSQL and create a database named `edu_system`.
- [x] Create a backend directory (`backend`) in the project root.
- [x] Set up a virtual environment: `python -m venv venv` and activate it.
- [ ] Install dependencies: `pip install django psycopg2-binary django-rest-framework`.
- [ ] Initialize a Django project: `django-admin startproject project .`.
- [ ] Create a Django app: `python manage.py startapp app`.
- [x] Configure PostgreSQL in `project/settings.py` with database credentials.
- [ ] Add `rest_framework` and `app` to `INSTALLED_APPS` in `project/settings.py`.

## Database and Models
- [ ] Define models in `app/models.py` for core ERD entities:
  - [x] `User` (extend `AbstractUser` with `role`, `phone_number`, etc.).
  - [x] `Student` (with `level`, `birth_date`, etc.).
  - [x] `Center` (with `name`, `address`, etc.).
  - [ ] `Notification` (with `type`, `content`, etc.).
  - [ ] `Log` (with `action`, `timestamp`, etc.).
- [ ] Generate migrations: `python manage.py makemigrations`.
- [ ] Apply migrations: `python manage.py migrate`.
- [ ] Create superuser for admin access: `python manage.py createsuperuser`.

## API Development
- [ ] Create serializers in `app/serializers.py` for core models (e.g., `StudentSerializer`, `NotificationSerializer`).
- [ ] Implement viewsets in `app/views.py` for core entities using Django REST Framework.
- [ ] Set up URL routing in `project/urls.py` and `app/urls.py` for API endpoints (e.g., `/api/students/`, `/api/notifications/`).
- [ ] Test API endpoints using Postman or `curl` to ensure CRUD operations work.

## Authentication
- [ ] Configure DRF token authentication in `project/settings.py`.
- [ ] Set up login endpoint using DRF’s `ObtainAuthToken` view.
- [ ] Test authentication by obtaining a token via the login endpoint.

## Notifications
- [ ] Install Twilio SDK: `pip install twilio`.
- [ ] Create a notification service in `app/services.py` for sending email (`smtplib`) and SMS (Twilio).
- [ ] Integrate notification service with `Notification` model to trigger messages on create/update.
- [ ] Test notification sending for a sample event (e.g., student registration).

## Logging
- [x] Create a logging middleware in `app/middleware.py` to record user actions in the `Log` model.
- [ ] Add middleware to `project/settings.py` under `MIDDLEWARE`.
- [ ] Test logging by performing actions (e.g., create student) and checking `Log` entries in the admin panel.

## Testing
- [ ] Install `pytest`: `pip install pytest pytest-django`.
- [ ] Write unit tests in `app/tests.py` for models and API endpoints.
- [ ] Run tests: `pytest`.
- [ ] Manually test critical flows (e.g., student creation, notification sending) via the Django admin panel.

## Deployment Preparation
- [ ] Add `gunicorn` and `django-cors-headers` to dependencies: `pip install gunicorn django-cors-headers`.
- [ ] Configure CORS in `project/settings.py` to allow frontend access.
- [ ] Create a `Procfile` for Heroku: `web: gunicorn project.wsgi`.
- [ ] Test locally: `python manage.py runserver` and verify APIs.