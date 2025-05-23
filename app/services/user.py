from sqlalchemy.orm import Session
from typing import Optional, List, Type, TypeVar, Generic, Any
from app.models.user import User, Role
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.parent import Parent
from app.schemas.user import UserCreate, UserUpdate
from app.config.security import hash_password

# Type variable for generic CRUD operations
T = TypeVar('T')


def create_user_with_role(db: Session, user_data: UserCreate, role: Role, extra_data: dict = None):
    extra_data = extra_data or {}

    # Determine the correct model class based on the role
    model_class = {
        Role.student: Student,
        Role.teacher: Teacher,
        Role.parent: Parent
    }.get(role, User)

    # Create an instance of the appropriate model
    user = model_class(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=role,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        phone_number=user_data.phone_number,
        address=user_data.address,
        notification_preference=user_data.notification_preference,
        status=user_data.status,
        **extra_data
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a base user with common fields"""
    db_user = {
        "type": "user"  # Set the polymorphic identity
    }

    return create_user_with_role(db, user_data, Role.admin, db_user)


def create_teacher(db: Session, user_data: UserCreate, teacher_data: dict) -> Teacher:
    """Create a teacher (inherits from User)"""
    db_teacher = {
        # Teacher-specific fields
        "center_id": teacher_data.get('center_id'),
        "qualifications": teacher_data.get('qualifications'),
        "specialization": teacher_data.get('specialization'),
        "years_of_experience": teacher_data.get('years_of_experience'),
        "certifications": teacher_data.get('certifications'),
        "availability": teacher_data.get('availability')
    }

    return create_user_with_role(db, user_data, Role.teacher, db_teacher)


def create_student(db: Session, user_data: UserCreate, student_data: dict) -> Student:
    """Create a student (inherits from User)"""
    db_student = {
        # Student-specific fields
        "level":student_data.get('level'),
        "exemption_status":student_data.get('exemption_status'),
        "center_id":student_data.get('center_id'),
        "birth_date":student_data.get('birth_date'),
        "gender":student_data.get('gender'),
        "nationality":student_data.get('nationality'),
        "id_number":student_data.get('id_number'),
        "parent_name":student_data.get('parent_name'),
        "parent_phone":student_data.get('parent_phone'),
        "emergency_contact":student_data.get('emergency_contact'),
        "medical_conditions":student_data.get('medical_conditions'),
        "registration_date":student_data.get('registration_date'),
        "previous_education":student_data.get('previous_education')
    }
    return create_user_with_role(db, user_data, Role.student, db_student)


def create_parent(db: Session, user_data: UserCreate, parent_data: dict) -> Parent:
    """Create a parent (inherits from User)"""
    db_parent = Parent(
        # Parent-specific fields
        occupation=parent_data.get('occupation'),
        relationship_to_student=parent_data.get('relationship_to_student'),
        emergency_contact=parent_data.get('emergency_contact'),
        preferred_contact_time=parent_data.get('preferred_contact_time'),
        notes=parent_data.get('notes')
    )

    return create_user_with_role(db, user_data, Role.parent, db_parent)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get a list of users"""
    return db.query(User).offset(skip).limit(limit).all()


def get_users_by_role(db: Session, role: Role, skip: int = 0, limit: int = 100) -> List[User]:
    """Get users filtered by role"""
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """Update a user's information"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    # Update user attributes that are provided
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
