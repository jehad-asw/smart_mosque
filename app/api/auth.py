from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, User, Role
from app.schemas.teacher import TeacherCreate, Teacher
from app.schemas.student import StudentCreate, Student
from app.schemas.parent import ParentCreate, Parent
from app.config.security import verify_password, create_access_token
from app.crud import user as user_crud
from app.deps.db import get_db, get_current_user
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User as UserModel
from typing import Dict, Any, Union

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a basic user"""
    if user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return user_crud.create_user(db, user)


@router.post("/register/teacher", response_model=Teacher)
def register_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    """Register a teacher (inherits from User)"""
    if user_crud.get_user_by_email(db, teacher.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_crud.get_user_by_username(db, teacher.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Extract teacher-specific fields
    teacher_data = {
        "qualifications": teacher.qualifications,
        "center_id": teacher.center_id,
        "specialization": teacher.specialization,
        "years_of_experience": teacher.years_of_experience,
        "certifications": teacher.certifications,
        "availability": teacher.availability
    }
    
    return user_crud.create_teacher(db, teacher, teacher_data)


@router.post("/register/student", response_model=Student)
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Register a student (inherits from User)"""
    if user_crud.get_user_by_email(db, student.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_crud.get_user_by_username(db, student.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Extract student-specific fields
    student_data = {
        "level": student.level,
        "exemption_status": student.exemption_status,
        "center_id": student.center_id,
        "birth_date": student.birth_date,
        "gender": student.gender,
        "nationality": student.nationality,
        "id_number": student.id_number,
        "parent_name": student.parent_name,
        "parent_phone": student.parent_phone,
        "emergency_contact": student.emergency_contact,
        "medical_conditions": student.medical_conditions,
        "registration_date": student.registration_date,
        "preferred_circle_id": student.preferred_circle_id,
        "previous_education": student.previous_education
    }
    
    return user_crud.create_student(db, student, student_data)


@router.post("/register/parent", response_model=Parent)
def register_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    """Register a parent (inherits from User)"""
    if user_crud.get_user_by_email(db, parent.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_crud.get_user_by_username(db, parent.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Extract parent-specific fields
    parent_data = {
        "occupation": parent.occupation,
        "relationship_to_student": parent.relationship_to_student,
        "emergency_contact": parent.emergency_contact,
        "preferred_contact_time": parent.preferred_contact_time,
        "notes": parent.notes
    }
    
    return user_crud.create_parent(db, parent, parent_data)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login a user and return a JWT token"""
    db_user = user_crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token with user ID, email, and role for authorization purposes
    token_data = {
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role.value,
        "type": db_user.type
    }
    token = create_access_token(data=token_data)
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def me(current_user: UserModel = Depends(get_current_user)):
    """Get the current logged-in user's information"""
    return current_user
