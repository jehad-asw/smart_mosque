from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, User
from app.schemas.teacher import TeacherCreate, Teacher
from app.schemas.student import StudentCreate, Student
from app.schemas.parent import ParentCreate, Parent
from app.config.security import (
    verify_password, create_token_pair, validate_password,
    verify_token, revoke_token, Token, MAX_LOGIN_ATTEMPTS,
    LOGIN_TIMEOUT_MINUTES
)
from app.services import user as user_crud
from app.deps.db import get_db, get_current_user
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User as UserModel
from datetime import datetime, timedelta
from typing import Dict
from collections import defaultdict
import time

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Rate limiting storage (using in-memory defaultdict)
login_attempts = defaultdict(list)

def check_rate_limit(email: str) -> None:
    """Check if user has exceeded login attempts"""
    now = time.time()
    # Remove attempts older than timeout window
    login_attempts[email] = [
        attempt for attempt in login_attempts[email]
        if now - attempt < LOGIN_TIMEOUT_MINUTES * 60
    ]
    
    if len(login_attempts[email]) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Please try again after {LOGIN_TIMEOUT_MINUTES} minutes"
        )

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a basic user with password validation"""
    if not validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain letters, numbers, and special characters"
        )
    
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


@router.post("/login", response_model=Token)
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    """Login user with rate limiting"""
    check_rate_limit(user.email)
    
    db_user = user_crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        # Record failed attempt
        login_attempts[user.email].append(time.time())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Clear login attempts on successful login
    if user.email in login_attempts:
        del login_attempts[user.email]
    
    # Create token pair
    token_data = {
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role.value,
        "type": db_user.type
    }
    access_token, refresh_token = create_token_pair(token_data)
    
    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Depends(oauth2_scheme)
):
    """Get new access token using refresh token"""
    try:
        payload = verify_token(refresh_token, is_refresh_token=True)
        db_user = user_crud.get_user_by_email(db, payload["sub"])
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Create new token pair
        token_data = {
            "sub": db_user.email,
            "user_id": db_user.id,
            "role": db_user.role.value,
            "type": db_user.type
        }
        new_access_token, new_refresh_token = create_token_pair(token_data)
        
        # Revoke old refresh token
        revoke_token(refresh_token)
        
        # Set new refresh token in cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7 * 24 * 60 * 60
        )
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    response: Response,
    token: str = Depends(oauth2_scheme),
    refresh_token: str = Depends(lambda x: x.cookies.get("refresh_token"))
):
    """Logout user and revoke tokens"""
    # Revoke both tokens
    revoke_token(token)
    if refresh_token:
        revoke_token(refresh_token)
    
    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        secure=True,
        httponly=True,
        samesite="strict"
    )
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
def me(current_user: UserModel = Depends(get_current_user)):
    """Get current user's information"""
    return current_user
