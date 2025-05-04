from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.student import Student
from app.schemas.student import StudentCreate
from app.crud.user import create_user_with_role
from app.models.user import Role
from typing import List, Optional

def create_student(db: Session, user_id: int, student: StudentCreate) -> Student:
    """Create a new student"""
    # Create user first since Student inherits from User
    student_dict = student.dict(exclude={'password'})
    db_student = Student(**student_dict)
    db_student.role = Role.student
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_user(db: Session, user_id: int) -> Optional[Student]:
    """Get a student by user ID"""
    return db.query(Student).filter(Student.id == user_id).first()

def get_student_by_id(db: Session, student_id: int) -> Optional[Student]:
    """Get a student by their ID"""
    return db.query(Student).filter(Student.id == student_id).first()

def get_students_by_name(db: Session, name: str) -> List[Student]:
    """Search for students by name"""
    return db.query(Student).filter(
        or_(
            Student.firstname.ilike(f"%{name}%"),
            Student.lastname.ilike(f"%{name}%")
        )
    ).all()

def get_all_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    """Get all students with pagination"""
    return db.query(Student).filter(Student.role == Role.student).offset(skip).limit(limit).all()
