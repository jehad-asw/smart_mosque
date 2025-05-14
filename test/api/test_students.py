from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import pytest
from app.api.students import router
from app.models.user import Role, User 
from app.schemas.student import Student
from app.services import student as student_crud
from app.deps.db import get_current_user, get_db
from datetime import datetime, timezone, timedelta
from jose import jwt
from test.utils import create_mock_student
from app.config.security import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

client = TestClient(router)

def create_test_token(email: str, user_id: int, role: str) -> str:
    """Helper function to create a test JWT token"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Short expiration for tests
    return jwt.encode(
        {
            "sub": email,
            "user_id": user_id,
            "role": role,
            "exp": int(expire.timestamp())  # Convert to integer timestamp
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@pytest.fixture
def mock_students():
    """Fixture that returns a list of mock students"""
    now = datetime.now(timezone.utc).isoformat()
    return [
        create_mock_student(
            id=1,
            username="student1",
            firstname="Student",
            lastname="One",
            email="student1@example.com",
            created_at=now,
            updated_at=now
        ),
        create_mock_student(
            id=2,
            username="student2",
            firstname="Student",
            lastname="Two",
            email="student2@example.com",
            created_at=now,
            updated_at=now
        )
    ]

@pytest.fixture
def mock_student():
    """Fixture that returns a single mock student"""
    now = datetime.now(timezone.utc).isoformat()
    return create_mock_student(
        id=1,
        username="student1",
        firstname="Student",
        lastname="One",
        email="student1@example.com",
        created_at=now,
        updated_at=now
    )

@pytest.fixture
def mock_db_session():
    """Fixture that provides a mock database session"""
    return MagicMock()

@pytest.fixture
def auth_headers(mock_student):
    """Fixture that returns authorization headers with a valid JWT token"""
    token = create_test_token(mock_student.email, mock_student.id, "student")
    return {"Authorization": f"Bearer {token}"}

def test_get_students(mock_students, auth_headers, mock_db_session):
    student_crud.get_all_students = MagicMock(return_value=mock_students)
    with patch('app.deps.db.get_current_user', return_value=mock_students[0]):
        with patch('app.deps.db.get_db', return_value=mock_db_session):
            response = client.get("/", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data) == 2

            for i, student in enumerate(mock_students):
                assert response_data[i]["id"] == student.id
                assert response_data[i]["username"] == student.username
                assert response_data[i]["email"] == student.email
                assert response_data[i]["role"] == "student"
                assert response_data[i]["level"] == student.level

def test_get_student_profile_as_student(mock_student, auth_headers, mock_db_session):
    student_crud.get_student_by_user = MagicMock(return_value=mock_student)
    with patch('app.deps.db.get_current_user', return_value=mock_student):
        with patch('app.deps.db.get_db', return_value=mock_db_session):
            response = client.get("/profile/me", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()

            assert response_data["id"] == mock_student.id
            assert response_data["username"] == mock_student.username
            assert response_data["email"] == mock_student.email
            assert response_data["role"] == "student"
            assert response_data["level"] == mock_student.level

def test_get_student_profile_as_non_student(mock_student, mock_db_session):
    mock_teacher = create_mock_student(
        id=1,
        username="teacher1",
        firstname="Teacher",
        lastname="One",
        email="teacher1@example.com",
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat()
    )
    mock_teacher.role = Role.teacher

    token = create_test_token(mock_teacher.email, mock_teacher.id, "teacher")
    headers = {"Authorization": f"Bearer {token}"}

    with patch('app.deps.db.get_current_user', return_value=mock_teacher):
        with patch('app.deps.db.get_db', return_value=mock_db_session):
            response = client.get("/profile/me", headers=headers)
            assert response.status_code == 403
            assert response.json() == {"detail": "User is not a student"}

def test_get_student_by_id(mock_student, auth_headers, mock_db_session):
    student_crud.get_student_by_id = MagicMock(return_value=mock_student)
    with patch('app.deps.db.get_current_user', return_value=mock_student):
        with patch('app.deps.db.get_db', return_value=mock_db_session):
            response = client.get(f"/{mock_student.id}", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()

            assert response_data["id"] == mock_student.id
            assert response_data["username"] == mock_student.username
            assert response_data["email"] == mock_student.email
            assert response_data["role"] == "student"
            assert response_data["level"] == mock_student.level

def test_get_students_by_name(mock_students, auth_headers, mock_db_session):
    student_crud.get_students_by_name = MagicMock(return_value=mock_students)
    with patch('app.deps.db.get_current_user', return_value=mock_students[0]):
        with patch('app.deps.db.get_db', return_value=mock_db_session):
            response = client.get("/search/Student", headers=auth_headers)
            assert response.status_code == 200
            response_data = response.json()

            for i, student in enumerate(mock_students):
                assert response_data[i]["id"] == student.id
                assert response_data[i]["username"] == student.username
                assert response_data[i]["email"] == student.email
                assert response_data[i]["role"] == "student"
                assert response_data[i]["level"] == student.level


