from sqlalchemy import Column, Integer, ForeignKey, String
from app.config.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    telephone = Column(String)
    address = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
