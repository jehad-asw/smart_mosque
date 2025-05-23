from datetime import date
import pytest
from sqlalchemy.orm import Session
from app.services.student import create_student, get_student_by_user
from app.models.student import ExemptionStatus, Gender, Student
from app.schemas.student import StudentCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_student(db_session: Session):
    user_id = 1
    student_data = StudentCreate(
        email="teststudent@example.com",
        username="teststudent",
        firstname="jehnny",
        lastname="Student",
        password= "paasword123",
        role="student",
        level="beginner",
        exemption_status=ExemptionStatus.non_exempted,
        center_id=1,
        birth_date=date(2005, 5, 15),
        gender=Gender.male,
        nationality="land",
        id_number="123456789",
        parent_name="Parent Name",
        parent_phone="123-456-7890",
        emergency_contact="987-654-3210",
        medical_conditions="None",
        registration_date=date(2025, 4, 1),
        previous_education="High School"
    )
    created_student = create_student(db_session, user_id, student_data)

    assert created_student.id is not None
    assert created_student.user_id == user_id
    assert created_student.email == "teststudent@example.com"
    assert created_student.username == "teststudent"
    assert created_student.firstname == "jehnny"
    assert created_student.lastname == "Student"
    assert created_student.level == "beginner"
    assert created_student.exemption_status == ExemptionStatus.non_exempted
    assert created_student.center_id == 1
    assert created_student.nationality == "land"
    assert created_student.id_number == "123456789"

def test_get_student_by_user(db_session: Session):
    user_id = 1
    student_data = StudentCreate(
        email="teststudent@example.com",
        username="teststudent",
        firstname="jehnny",
        lastname="Student",
        password= "paasword123",
        role="student",
        level="beginner",
        exemption_status=ExemptionStatus.non_exempted,
        center_id=1,
        birth_date=date(2005, 5, 15),
        gender=Gender.male,
        nationality="land",
        id_number="123456789",
        parent_name="Parent Name",
        parent_phone="123-456-7890",
        emergency_contact="987-654-3210",
        medical_conditions="None",
        registration_date=date(2025, 4, 1),
        previous_education="High School"
    )
    create_student(db_session, user_id, student_data)

    fetched_student = get_student_by_user(db_session, user_id)

    assert fetched_student is not None
    assert fetched_student.user_id == user_id
    assert fetched_student.email == "teststudent@example.com"
    assert fetched_student.username == "teststudent"
    assert fetched_student.firstname == "jehnny"
    assert fetched_student.lastname == "Student"
    assert fetched_student.level == "beginner"
    assert fetched_student.exemption_status == ExemptionStatus.non_exempted
    assert fetched_student.center_id == 1
    assert fetched_student.nationality == "land"
    assert fetched_student.id_number == "123456789"