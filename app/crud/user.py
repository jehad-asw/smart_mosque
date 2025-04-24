from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.config.security import hash_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update(db: Session, id: int, user: User):
    user.id = id
    db.merge(user)
    db.commit()
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
    db.flush()
