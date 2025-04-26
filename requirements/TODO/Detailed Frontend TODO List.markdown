# Detailed Frontend TODO List (React)

## 1. Setup Environment
- [ ] Install Node.js 18+ and verify.
- [ ] Create frontend directory and initialize React with Vite.
- [ ] Install dependencies: `axios`, `@mui/material`, `react-router-dom`.
- [ ] Start development server and verify setup.

## 2. Project Structure
- [ ] Create `src/components` for reusable components (e.g., `DataTable`, `FormInput`).
- [ ] Create `src/pages` for page-level components (e.g., `Login`, `StudentList`).
- [ ] Configure Material-UI theme for consistent styling.

## 3. Authentication Pages
- [ ] **Login Page**:
  - [ ] Build form with username and password.
  - [ ] Implement API call to `/api/token/` and store token.
- [ ] **Register Page**:
  - [ ] Build form for user registration.
  - [ ] Implement API call to `/api/register/`.

## 4. Dashboard
- [ ] Create `Dashboard` page:
  - [ ] Fetch and display metrics from `/api/dashboard/` (e.g., student count).
  - [ ] Show recent notifications from `/api/notifications/`.

## 5. Entity Management Pages (CRUD)
- [ ] **Students**:
  - [ ] `StudentList`: Fetch and display students from `/api/students/`.
  - [ ] `StudentForm`: Create and edit students, POST/PUT to `/api/students/`.
- [ ] **Centers**:
  - [ ] `CenterList`: Fetch and display centers.
  - [ ] `CenterForm`: Create and edit centers.
- [ ] **Teachers**:
  - [ ] `TeacherList`: Fetch and display teachers.
  - [ ] `TeacherForm`: Create and edit teachers.
- [ ] **Study Circles**:
  - [ ] `StudyCircleList`: Fetch and display circles.
  - [ ] `StudyCircleForm`: Create and edit circles.
- [ ] **Notifications**:
  - [ ] `NotificationList`: Fetch and display notifications.
  - [ ] `NotificationForm`: Create notifications, POST to `/api/notifications/`.
- [ ] **Schedules**:
  - [ ] `ScheduleList`: Fetch and display schedules.
  - [ ] `ScheduleForm`: Create and edit schedules.
- [ ] **Tests**:
  - [ ] `TestList`: Fetch and display tests.
  - [ ] `TestForm`: Create and edit tests.
- [ ] **Subscriptions**:
  - [ ] `SubscriptionList`: Fetch and display subscriptions.
  - [ ] `SubscriptionForm`: Create and edit subscriptions.
- [ ] **Logs**:
  - [ ] `LogList`: Fetch and display logs (read-only).

## 6. Custom Features
- [ ] **Notification Sending**:
  - [ ] Create a button or form to trigger `/api/send-notification/`.
- [ ] **Parent Management**:
  - [ ] `ParentList`: Fetch and display parents.
  - [ ] `ParentForm`: Create and edit parents.
- [ ] **Permissions**:
  - [ ] `PermissionList`: Fetch and display permissions.
  - [ ] `RolePermissionForm`: Assign permissions to roles.

## 7. Routing
- [ ] Configure routes for all pages (e.g., `/login`, `/students`, `/dashboard`).
- [ ] Implement protected routes for authenticated users.

## 8. API Integration
- [ ] Create an API service (e.g., `api.js`) with Axios, including token authentication.
- [ ] Implement API calls in components for fetching and updating data.

## 9. Testing
- [ ] Write unit tests for components (e.g., `StudentForm` rendering).
- [ ] Test API integrations manually (e.g., form submission, data display).
- [ ] Verify notification polling or WebSocket functionality.

## 10. Deployment Preparation
- [ ] Create production build: `npm run build`.
- [ ] Configure environment variables for API URL.
- [ ] Test build locally and ensure token headers are set.