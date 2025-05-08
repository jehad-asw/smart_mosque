from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.center import get_center, get_centers, create_center, update_center, delete_center
from app.deps.db import get_db
from app.schemas.center import CenterCreate, CenterUpdate, Center

router = APIRouter()


@router.get("/centers/{id}", response_model=Center)
def read_center(id: int, db: Session = Depends(get_db)):
    db_center = get_center(db, id)
    if not db_center:
        raise HTTPException(status_code=404, detail="Center not found")
    return db_center

@router.get("/centers", response_model=list[Center])
def read_centers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_centers(db, skip=skip, limit=limit)

@router.post("/centers", response_model=Center)
def create_new_center(center: CenterCreate, db: Session = Depends(get_db)):
    return create_center(db, center)

@router.put("/centers/{id}", response_model=Center)
def update_existing_center(id: int, center: CenterUpdate, db: Session = Depends(get_db)):
    db_center = update_center(db, id, center)
    if not db_center:
        raise HTTPException(status_code=404, detail="Center not found")
    return db_center

@router.delete("/centers/{id}", response_model=Center)
def delete_existing_center(id: int, db: Session = Depends(get_db)):
    db_center = delete_center(db, id)
    if not db_center:
        raise HTTPException(status_code=404, detail="Center not found")
    return db_center