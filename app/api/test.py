from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.test import TestCreate, TestUpdate, TestResponse
from app.crud.test import create_test, update_test, delete_test, get_all_tests, get_test_by_id
from app.deps.db import get_db

router = APIRouter()

@router.post("/tests", response_model=TestResponse)
def create_test_endpoint(test: TestCreate, db: Session = Depends(get_db)):
    return create_test(db, test)

@router.put("/tests/{id}", response_model=TestResponse)
def update_test_endpoint(id: int, test: TestUpdate, db: Session = Depends(get_db)):
    db_test = get_test_by_id(db, id)
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    return update_test(db, id, test)

@router.delete("/tests/{id}")
def delete_test_endpoint(id: int, db: Session = Depends(get_db)):
    db_test = get_test_by_id(db, id)
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    delete_test(db, id)
    return {"message": "Test deleted successfully"}

@router.get("/tests", response_model=list[TestResponse])
def get_all_tests_endpoint(db: Session = Depends(get_db)):
    return get_all_tests(db)

@router.get("/tests/{id}", response_model=TestResponse)
def get_test_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    db_test = get_test_by_id(db, id)
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test