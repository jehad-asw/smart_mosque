from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.api.teachers import router
from app.models.user import Role
from app.schemas.teacher import Teacher

client = TestClient(router)

def test_get_teachers():
    # Mock the database session and user_crud.get_users_by_role
    mock_db = MagicMock(spec=Session)
    mock_teachers = [
        Teacher(id=1, name="Teacher 1", role=Role.teacher),
        Teacher(id=2, name="Teacher 2", role=Role.teacher),
    ]
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_teachers

    # Mock user_crud.get_users_by_role
    with MagicMock() as mock_user_crud:
        mock_user_crud.get_users_by_role.return_value = mock_teachers

        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "name": "Teacher 1", "role": "teacher"},
            {"id": 2, "name": "Teacher 2", "role": "teacher"},
        ]

def test_get_teacher_profile():
    # Mock the current user
    mock_current_user = Teacher(id=1, name="Teacher 1", role=Role.teacher)

    # Mock require_role
    with MagicMock() as mock_require_role:
        mock_require_role.return_value = mock_current_user

        response = client.get("/me")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "Teacher 1", "role": "teacher"}