from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    tester_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    date = Column(Date, nullable=False)
    result = Column(String, nullable=False)
    level = Column(String, nullable=False)

    student = relationship("Student", back_populates="tests")
    tester = relationship("Teacher", back_populates="tests")