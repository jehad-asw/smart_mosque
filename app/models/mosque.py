from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from app.config.database import Base

# Association tables
teacher_mosque_association = Table(
    'teacher_mosque', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True),
    Column('mosque_id', Integer, ForeignKey('mosques.id'), primary_key=True)
)

student_mosque_association = Table(
    'student_mosque', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('mosque_id', Integer, ForeignKey('mosques.id'), primary_key=True)
)

class Mosque(Base):
    __tablename__ = "mosques"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    center_id = Column(Integer, ForeignKey('centers.id'))

    # Relationships
    center = relationship("Center", back_populates="mosques")
    teachers = relationship("Teacher", secondary=teacher_mosque_association, back_populates="mosques")
    students = relationship("Student", secondary=student_mosque_association, back_populates="mosques")
    study_circles = relationship("StudyCircle", back_populates="mosque")
