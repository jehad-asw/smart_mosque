from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.student import Student, StudentUpdate
from app.crud import student as student_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/profile/me", response_model=Student)
async def get_student_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Get the current student's profile"""
    if current_user.role != Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a student"
        )
    student = student_crud.get_student_by_user(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student

@router.get("/search/{name}", response_model=List[Student])
async def search_students(
    name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Search for students by name"""
    students = student_crud.get_students_by_name(db, name)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

@router.get("/{student_id}", response_model=Student)
async def get_student_by_id(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Get a student by ID"""
    student = student_crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/", response_model=List[Student])
async def get_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    skip: int = 0,
    limit: int = 100
):
    """Get a list of all students"""
    students = student_crud.get_all_students(db, skip=skip, limit=limit)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

@router.put("/students/{student_id}", response_model=Student)
def update_existing_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = student_crud.update_student(db, student_id, student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/students/{student_id}", response_model=Student)
def delete_existing_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_crud.delete_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="student not found")
    return db_student