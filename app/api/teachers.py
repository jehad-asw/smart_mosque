from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.teacher import TeacherCreate, Teacher, TeacherUpdate
from app.crud import user as user_crud
from app.crud import teacher as teacher_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/", response_model=List[Teacher])
def get_teachers(
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    skip: int = 0, 
    limit: int = 100
):
    """Get a list of all teachers"""
    return user_crud.get_users_by_role(db, Role.teacher, skip, limit)

@router.get("/me", response_model=Teacher)
def get_teacher_profile(
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Get the current teacher's profile"""
    if current_user.role != Role.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a teacher"
        )
    return current_user


@router.put("/teachers/{teacher_id}", response_model=Teacher)
def update_existing_teacher(teacher_id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.update_teacher(db, teacher_id, teacher)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return db_teacher


@router.delete("/teachers/{teacher_id}", response_model=Teacher)
def delete_existing_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.delete_teacher(db, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return db_teacher