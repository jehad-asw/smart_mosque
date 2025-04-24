from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate


def create_student(db: Session, user_id: int, student: StudentCreate):
    db_student = Student(**student.dict(), user_id=user_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student_by_user(db: Session, user_id: int):
    return db.query(Student).filter(Student.user_id == user_id).first()
