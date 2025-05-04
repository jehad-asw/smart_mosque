from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.parent import ParentCreate, Parent, ParentUpdate
from app.crud import user as user_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/", response_model=List[Parent])
def get_parents(
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    skip: int = 0, 
    limit: int = 100
):
    """Get a list of all parents"""
    return user_crud.get_users_by_role(db, Role.parent, skip, limit)

@router.get("/me", response_model=Parent)
def get_parent_profile(
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Get the current parent's profile"""
    if current_user.role != Role.parent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a parent"
        )
    return current_user
