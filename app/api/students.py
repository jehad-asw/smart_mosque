from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.student import StudentCreate, StudentRead
from app.crud import student as student_crud
from app.deps.db import get_db, get_current_user


router = APIRouter()


@router.post("/", response_model=StudentRead)
def register_student(student_in: StudentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return student_crud.create_student(db=db, user_id=user.id, student=student_in)


@router.get("/me", response_model=StudentRead)
def get_my_student_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return student_crud.get_student_by_user(db=db, user_id=user.id)
