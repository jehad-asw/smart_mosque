from sqlalchemy.orm import Session
from app.models.test import Test
from app.schemas.test import TestCreate, TestUpdate

def create_test(db: Session, test: TestCreate) -> Test:
    db_test = Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def update_test(db: Session, id: int, test: TestUpdate) -> Test:
    db_test = db.query(Test).filter(Test.id == id).first()
    if not db_test:
        return None
    for key, value in test.dict().items():
        setattr(db_test, key, value)
    db.commit()
    db.refresh(db_test)
    return db_test

def delete_test(db: Session, id: int):
    db_test = db.query(Test).filter(Test.id == id).first()
    if db_test:
        db.delete(db_test)
        db.commit()

def get_all_tests(db: Session):
    return db.query(Test).all()

def get_test_by_id(db: Session, id: int) -> Test:
    return db.query(Test).filter(Test.id == id).first()