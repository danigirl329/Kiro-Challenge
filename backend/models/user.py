from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    userId: str
    name: str = Field(..., min_length=1, max_length=200)
    createdAt: str
    updatedAt: str


class UserCreate(BaseModel):
    userId: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=200)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
