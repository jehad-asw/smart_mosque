from sqlalchemy import Column, Integer, ForeignKey, String, Date, Enum, Text
from sqlalchemy.orm import relationship
from app.models.user import User
import enum
from datetime import date, datetime


class ExemptionStatus(str, enum.Enum):
    exempted = "exempted"
    non_exempted = "non-exempted"
    partial = "partial"


class Gender(str, enum.Enum):
    male = "male"
    female = "female"


class Student(User):
    """Student model that inherits from User"""
    __tablename__ = "students"

    # Link to parent User table
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Student-specific fields
    level = Column(String)
    exemption_status = Column(Enum(ExemptionStatus), default=ExemptionStatus.non_exempted)
    center_id = Column(Integer, ForeignKey("centers.id"))
    birth_date = Column(Date, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    nationality = Column(String, nullable=True)
    id_number = Column(String, nullable=True)
    parent_name = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    registration_date = Column(Date, default=datetime.utcnow)
    preferred_circle_id = Column(Integer, ForeignKey("study_circles.id"), nullable=True)
    previous_education = Column(String, nullable=True)

    # Relationships
    center = relationship("Center", back_populates="students")
    preferred_circle = relationship("StudyCircle", back_populates="students")
    student_circles = relationship("CircleStudent", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    student_parents = relationship("StudentParent", back_populates="student")
    mosques = relationship("Mosque", secondary="student_mosque", back_populates="students")

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.user.date_of_birth.year - (
                (today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day)
        )

    @property
    def full_name(self) -> str:
        return f"{self.user.firstname} {self.user.lastname}"
