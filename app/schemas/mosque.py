from pydantic import BaseModel
from typing import Optional


class MosqueBase(BaseModel):
    name: str
    address: str


class MosqueCreate(MosqueBase):
    pass


class MosqueUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class Mosque(MosqueBase):
    id: int

    class Config:
        orm_mode = True