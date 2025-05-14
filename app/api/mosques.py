from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.mosque import Mosque, MosqueCreate, MosqueUpdate
from app.services.mosque import (
    create_mosque,
    get_mosque_by_id,
    get_all_mosques,
    update_mosque,
    delete_mosque,
)
from app.deps.db import get_db

router = APIRouter()


@router.post("/", response_model=Mosque)
def create_new_mosque(mosque: MosqueCreate, db: Session = Depends(get_db)):
    return create_mosque(db, mosque)


@router.get("/{id}", response_model=Mosque)
def get_mosque(id: int, db: Session = Depends(get_db)):
    mosque = get_mosque_by_id(db, id)
    if not mosque:
        raise HTTPException(status_code=404, detail="Mosque not found")
    return mosque


@router.get("/", response_model=List[Mosque])
def get_all_mosques_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_mosques(db, skip=skip, limit=limit)


@router.put("/{id}", response_model=Mosque)
def update_existing_mosque(id: int, mosque: MosqueUpdate, db: Session = Depends(get_db)):
    updated_mosque = update_mosque(db, id, mosque.dict(exclude_unset=True))
    if not updated_mosque:
        raise HTTPException(status_code=404, detail="Mosque not found")
    return updated_mosque


@router.delete("/{id}", response_model=dict)
def delete_existing_mosque(id: int, db: Session = Depends(get_db)):
    success = delete_mosque(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Mosque not found")
    return {"detail": "Mosque deleted successfully"}