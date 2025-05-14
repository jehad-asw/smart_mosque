# Detailed Backend TODO List (Django)

## 1. Setup Environment
- [ ] Install Python 3.10+ and verify.
- [ ] Install PostgreSQL and create database `edu_system`.
- [ ] Create backend directory and set up virtual environment.
- [ ] Install dependencies: `django`, `psycopg2-binary`, `django-rest-framework`, `twilio`.
- [ ] Initialize Django project and app.
- [ ] Configure PostgreSQL in `settings.py`.
- [ ] Add `rest_framework` and app to `INSTALLED_APPS`.

## 2. Database Models
- [ ] Define models in `models.py` for all entities:
  - [x] `User` (with `role`, `phone_number`, etc.)
  - [x] `Center`
  - [x] `Teacher`
  - [x] `Student`
  - [ ] `Staff`
  - [x] `Parent`
  - [x] `StudyCircle`
  - [x] `CircleStudent`
  - [x] `Attendance`
  - [x] `Test`
  - [ ] `TestRequest`
  - [ ] `Subscription`
  - [ ] `Salary`
  - [ ] `CardCertificate`
  - [ ] `Notification`
  - [ ] `NotificationRecipient`
  - [ ] `Permission`
  - [ ] `RolePermission`
  - [ ] `Schedule`
  - [ ] `EducationalProject`
  - [ ] `Document`
  - [ ] `FinancialTransaction`
  - [ ] `Log`
- [ ] Generate and apply migrations.

## 3. API Endpoints (CRUD for Each Entity)
- [ ] Create serializers for all models.
- [ ] Implement viewsets for each entity:
  - [x] `/api/users/` (CRUD)
  - [x] `/api/centers/` (CRUD)
  - [x] `/api/teachers/` (CRUD)
  - [x] `/api/students/` (CRUD)
  - [ ] `/api/staff/` (CRUD)
  - [ ] `/api/parents/` (CRUD)
  - [x] `/api/study-circles/` (CRUD)
  - [??] `/api/circle-students/` (CRUD)
  - [x] `/api/attendance/` (CRUD)
  - [x] `/api/assignments/` (CRUD)
  - [x] `/api/centers/` (CRUD)
  - [x] `/api/mosques/` (CRUD)
  - [ ] `/api/test-requests/` (CRUD)
  - [ ] `/api/subscriptions/` (CRUD)
  - [ ] `/api/salaries/` (CRUD)
  - [ ] `/api/card-certificates/` (CRUD)
  - [ ] `/api/notifications/` (CRUD)
  - [ ] `/api/notification-recipients/` (CRUD)
  - [ ] `/api/permissions/` (CRUD)
  - [ ] `/api/role-permissions/` (CRUD)
  - [ ] `/api/schedules/` (CRUD)
  - [ ] `/api/educational-projects/` (CRUD)
  - [ ] `/api/documents/` (CRUD)
  - [ ] `/api/financial-transactions/` (CRUD)
  - [ ] `/api/logs/` (Read-only for auditing)
- [ ] Set up URL routing for all viewsets.

## 4. Custom Endpoints
- [ ] **Authentication**:
  - [x] `/api/token/` for obtaining auth token.
  - [x] `/api/register/` for user registration.
- [ ] **Notifications**:
  - [ ] `/api/send-notification/` to trigger notification sending.
- [ ] **Dashboard Metrics**:
  - [ ] `/api/dashboard/` to fetch aggregated data (e.g., student count, recent notifications).

## 5. Authentication and Permissions
- [ ] Configure DRF token authentication.
- [ ] Implement permission classes for role-based access (e.g., `IsManager`, `IsTeacher`).
- [ ] Apply permissions to viewsets (e.g., only managers can create centers).

## 6. Notifications Implementation
- [ ] Create a notification service for email and SMS.
- [ ] Integrate with `Notification` model to send messages on create.
- [ ] Schedule notifications using Celery or Django Q if needed.

## 7. Logging
- [ ] Implement logging middleware to record actions in `Log` model.
- [ ] Ensure logging for sensitive operations (e.g., student creation, test updates).

## 8. Testing
- [ ] Write unit tests for models and APIs.
- [ ] Test custom endpoints (e.g., login, notification sending).
- [ ] Use Django admin to verify data integrity.

## 9. Deployment Preparation
- [ ] Install `gunicorn` and `django-cors-headers`.
- [ ] Configure CORS for frontend domain.
- [ ] Create `Procfile` for Heroku deployment.
- [ ] Test locally with `runserver`.