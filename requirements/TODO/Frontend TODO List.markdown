# Frontend TODO List (React)

## Setup Environment
- [ ] Install Node.js 18+ and verify with `node --version`.
- [ ] Create a frontend directory (`frontend`) in the project root.
- [ ] Initialize a React project with Vite: `npm create vite@latest . -- --template react`.
- [ ] Install dependencies: `npm install axios @mui/material @emotion/react @emotion/styled react-router-dom`.
- [ ] Start the development server: `npm run dev` and verify the app runs locally.

## Project Structure
- [ ] Create a `src/components` directory for reusable components.
- [ ] Create a `src/pages` directory for page-level components (e.g., `Login`, `StudentForm`).
- [ ] Configure Material-UI theme in `src/index.jsx` for consistent styling.

## Core Pages
- [ ] Create `Login` page:
  - [ ] Add form with username and password fields using Material-UI `TextField`.
  - [ ] Implement login logic to call backend `/api/token/` endpoint and store token in `localStorage`.
- [ ] Create `StudentForm` page:
  - [ ] Build form with fields matching `Student` model (e.g., `name`, `birth_date`, `level`) using Material-UI.
  - [ ] Implement form submission to POST to `/api/students/` with token authentication.
- [ ] Create `Dashboard` page:
  - [ ] Display metrics (e.g., student count) fetched from `/api/students/` using Material-UI cards.
  - [ ] Add a section for recent notifications.

## Notifications
- [ ] Create `NotificationList` component:
  - [ ] Fetch notifications from `/api/notifications/` using Axios with token authentication.
  - [ ] Implement polling (every 60 seconds) to refresh notifications.
  - [ ] Display notifications in a Material-UI list.
- [ ] Add notification badge or alert on the dashboard for unread notifications.

## Routing
- [ ] Configure React Router in `src/App.jsx`.
- [ ] Define routes for `/login`, `/register`, `/dashboard`, and redirect unauthenticated users to `/login`.
- [ ] Test navigation between pages.

## Testing
- [ ] Write unit tests for components using Jest (e.g., test `StudentForm` rendering).
- [ ] Run tests: `npm test`.
- [ ] Manually test UI flows (e.g., login, form submission, notification display).
- [ ] Verify API integration by checking data flow from backend to frontend.

## Deployment Preparation
- [ ] Create a production build: `npm run build`.
- [ ] Test the build locally: `npm run preview`.
- [ ] Configure environment variable for backend API URL (e.g., `.env` with `VITE_API_URL`).
- [ ] Ensure token authentication headers are included in all API requests.