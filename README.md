# Educational and Quranic Institutes Management System

A comprehensive platform for managing educational activities in Islamic institutes and Quranic centers, inspired by the Furqan System. This system provides complete management for centers, teachers, students, study circles, attendance, tests, and financial operations.

## Project Vision

Develop an integrated management system that meets the needs of educational and Quranic institutes, facilitates administrative and educational processes, and provides an interactive environment connecting all stakeholders (administration, teachers, students).

## Features

### User and Access Management
- **Multi-level User System**: Support for administrators, center managers, teachers, students, and staff
- **Role-based Access Control**: Granular permissions system for different user roles
- **Authentication**: Secure login and registration with token-based authentication

### Educational Management
- **Centers Management**: Register and manage multiple educational centers
- **Teacher Management**: Track teacher qualifications, schedules, and performance
- **Student Management**: Comprehensive student profiles with academic progress tracking
- **Study Circles**: Create and manage individual or group-based study circles
- **Attendance Tracking**: Record and monitor student attendance
- **Educational Projects**: Assign and track educational projects and curricula

### Assessment and Certification
- **Testing System**: Create, conduct, and grade tests
- **Test Requests**: Process student and teacher test requests
- **Cards and Certificates**: Issue and manage student ID cards and certificates

### Financial Operations
- **Subscription Management**: Track student payments and subscriptions
- **Salary Management**: Process teacher and staff salaries
- **Financial Transactions**: Record and report on all financial activities

### Communication
- **Notification System**: Send automated notifications to users
- **Parent Portal**: Allow parents to monitor their children's progress

## Planned Technology Stack

### Backend
- **Framework**: Django with Django REST Framework
- **Database**: PostgreSQL for scalable data storage
- **Authentication**: Django's built-in authentication with JWT tokens
- **API**: RESTful API design following best practices

### Frontend
- **Framework**: React with functional components
- **UI Library**: Material-UI for consistent styling
- **State Management**: React hooks (useState, useEffect)
- **API Communication**: Axios for backend requests

## Current Implementation Status

The current repository contains a FastAPI-based backend prototype with the following components:

- Basic user authentication with JWT
- Teacher and student management
- SQLAlchemy ORM for database operations
- Alembic for database migrations

## Project Structure

```
smart_mosque/
├── alembic/              # Database migration scripts
├── app/
│   ├── api/             # API endpoints
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── teachers.py  # Teacher management endpoints
│   │   └── students.py  # Student management endpoints
│   ├── config/          # Application configuration
│   │   ├── database.py  # Database connection setup
│   │   └── security.py  # Authentication and security utilities
│   ├── crud/            # Database CRUD operations
│   ├── deps/            # Dependency injection
│   ├── models/          # SQLAlchemy models
│   │   ├── user.py      # User model with roles
│   │   ├── teacher.py   # Teacher model
│   │   └── student.py   # Student model
│   └── schemas/         # Pydantic schemas for validation
├── requirements/        # Project requirements and planning documents
│   ├── AIRules/         # Development guidelines
│   ├── ERD/             # Entity Relationship Diagrams
│   ├── TODO/            # Development task lists
│   └── systemTechnologies/ # Technology stack documentation
├── .env                 # Environment variables (not in version control)
├── alembic.ini          # Alembic configuration
├── create_db.py         # Database initialization script
└── docker-compose.yml   # Docker configuration for PostgreSQL
```

## Getting Started with the Current Backend

### Prerequisites

- Python 3.7+
- PostgreSQL (for production) or SQLite (for development)
- Docker and Docker Compose (optional, for PostgreSQL)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart_mosque.git
   cd smart_mosque
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/smart_mosque
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

### Database Setup

#### Using SQLite (Development)

1. Update the database URL in `app/config/database.py` to use SQLite:
   ```python
   DATABASE_URL = "sqlite:///./smartmosque.db"
   ```

2. Initialize the database:
   ```bash
   python create_db.py
   ```

#### Using PostgreSQL (Production)

1. Start PostgreSQL using Docker:
   ```bash
   docker-compose up -d
   ```

2. Initialize the database:
   ```bash
   python create_db.py
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the application:
   - API: http://127.0.0.1:8000
   - Swagger UI documentation: http://127.0.0.1:8000/docs
   - ReDoc documentation: http://127.0.0.1:8000/redoc

## Development Roadmap

### Phase 1: Backend Development
- Complete Django REST Framework setup
- Implement all database models according to ERD
- Develop authentication and permission system
- Create API endpoints for core functionality

### Phase 2: Frontend Development
- Set up React application with Material-UI
- Implement authentication flows
- Build dashboard and entity management interfaces
- Create forms for all CRUD operations

### Phase 3: Integration and Testing
- Connect frontend to backend APIs
- Implement real-time notifications
- Conduct user testing and gather feedback
- Fix bugs and optimize performance

## Development Guidelines

### Backend (Current FastAPI / Planned Django)
- Follow RESTful conventions for API routes
- Use ORM for all database queries; avoid raw SQL
- Name variables and functions in snake_case
- Store sensitive data in environment variables
- Implement logging for key operations

### Frontend (Planned React)
- Use functional components with React hooks
- Prefer Material-UI for styling; avoid custom CSS
- Use Axios for all API requests
- Name variables and functions in camelCase
- Follow ES6+ syntax best practices

## Contributors

- Initial development team
