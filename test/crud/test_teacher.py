import pytest
from sqlalchemy.orm import Session
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate
from app.crud.teacher import create_teacher, get_teacher_by_user

def test_create_teacher(db_session: Session):

    user_id = 1
    teacher_data = TeacherCreate(name="John Doe", subject="Math")
    
    created_teacher = create_teacher(db_session, user_id, teacher_data)  

    assert created_teacher.id is not None
    assert created_teacher.user_id == user_id
    assert created_teacher.name == teacher_data.name
    assert created_teacher.subject == teacher_data.subject


def test_get_teacher_by_user(db_session: Session):
   
    user_id = 2
    teacher_data = TeacherCreate(name="Jane Smith", subject="Science")
    created_teacher = create_teacher(db_session, user_id, teacher_data)
    
    fetched_teacher = get_teacher_by_user(db_session, user_id)
    
    assert fetched_teacher is not None
    assert fetched_teacher.id == created_teacher.id
    assert fetched_teacher.user_id == user_id
    assert fetched_teacher.name == teacher_data.name
    assert fetched_teacher.subject == teacher_data.subject