from datetime import datetime, timezone
from app.models.user import Role
from app.models.student import Student, ExemptionStatus, Gender
from unittest.mock import MagicMock
from typing import Optional

def create_mock_student(
    id: int,
    username: str,
    firstname: str,
    lastname: str,
    email: str,
    level: str = "beginner",
    created_at: Optional[str] = None,
    updated_at: Optional[str] = None
) -> MagicMock:
    """Create a mock student with default values"""
    now = datetime.now(timezone.utc).isoformat()
    mock_student = MagicMock(spec=Student)
    
    # Set all required attributes
    mock_student.id = id
    mock_student.username = username
    mock_student.firstname = firstname
    mock_student.lastname = lastname
    mock_student.email = email
    mock_student.role = Role.student
    mock_student.level = level
    mock_student.exemption_status = ExemptionStatus.non_exempted
    mock_student.created_at = created_at or now
    mock_student.updated_at = updated_at or now
    mock_student.type = "student"
    mock_student.phone_number = None
    mock_student.address = None
    mock_student.notification_preference = "email"
    mock_student.status = "active"
    mock_student.center_id = None
    mock_student.birth_date = None
    mock_student.gender = None
    mock_student.nationality = None
    mock_student.id_number = None
    mock_student.parent_name = None
    mock_student.parent_phone = None
    mock_student.emergency_contact = None
    mock_student.medical_conditions = None
    mock_student.registration_date = None
    mock_student.preferred_circle_id = None
    mock_student.previous_education = None

    # Add model-to-dict conversion for response serialization
    mock_student.dict = lambda **kwargs: {
        "id": mock_student.id,
        "username": mock_student.username,
        "firstname": mock_student.firstname,
        "lastname": mock_student.lastname,
        "email": mock_student.email,
        "role": mock_student.role,
        "level": mock_student.level,
        "created_at": mock_student.created_at,
        "updated_at": mock_student.updated_at,
        "type": mock_student.type,
        "exemption_status": mock_student.exemption_status,
        "phone_number": mock_student.phone_number,
        "address": mock_student.address,
        "notification_preference": mock_student.notification_preference,
        "status": mock_student.status,
        "center_id": mock_student.center_id,
        "birth_date": mock_student.birth_date,
        "gender": mock_student.gender,
        "nationality": mock_student.nationality,
        "id_number": mock_student.id_number,
        "parent_name": mock_student.parent_name,
        "parent_phone": mock_student.parent_phone,
        "emergency_contact": mock_student.emergency_contact,
        "medical_conditions": mock_student.medical_conditions,
        "registration_date": mock_student.registration_date,
        "preferred_circle_id": mock_student.preferred_circle_id,
        "previous_education": mock_student.previous_education
    }
    
    return mock_student