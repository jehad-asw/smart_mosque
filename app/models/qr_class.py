from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time
from sqlalchemy.orm import relationship
from app.config.database import Base


class QrClass(Base):
    __table__ = "qr_class"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # need to create a random name from a list
    code = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    max_students = Column(Integer)

    mosque_id = Column(Integer, ForeignKey("mosques.id"), unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), unique=True)
