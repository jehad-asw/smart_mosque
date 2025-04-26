# Smart Mosque - Educational Management System

A modern web application for managing educational activities in mosques, including teacher and student management with role-based access control.

## Features

- **User Authentication**: Secure login and registration with JWT token-based authentication
- **Role-Based Access Control**: Different access levels for administrators, teachers, and students
- **Teacher Management**: Complete CRUD operations for teacher records
- **Student Management**: Track and manage student information and classes
- **RESTful API**: Well-structured API endpoints following REST principles
- **Database Integration**: Persistent storage with SQLAlchemy ORM

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: Passlib with bcrypt
- **Database Migrations**: Alembic
- **API Documentation**: Swagger UI and ReDoc (auto-generated)

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
├── .env                 # Environment variables (not in version control)
├── alembic.ini          # Alembic configuration
├── create_db.py         # Database initialization script
└── docker-compose.yml   # Docker configuration for PostgreSQL
```

## Getting Started

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

## API Endpoints

### Authentication

- `POST /token` - Login and get access token
- `POST /users/` - Register a new user

### Teachers

- `GET /teachers/` - List all teachers
- `POST /teachers/` - Create a new teacher
- `GET /teachers/{id}` - Get a specific teacher
- `PUT /teachers/{id}` - Update a teacher
- `DELETE /teachers/{id}` - Delete a teacher

### Students

- `GET /students/` - List all students
- `POST /students/` - Create a new student
- `GET /students/{id}` - Get a specific student
- `PUT /students/{id}` - Update a student
- `DELETE /students/{id}` - Delete a student

## Development

### Database Migrations

To create a new migration after model changes:

```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:

```bash
alembic upgrade head
```

## Security

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- Environment variables for sensitive information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name - Initial work
