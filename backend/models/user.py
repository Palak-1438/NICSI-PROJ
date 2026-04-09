from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CITIZEN = "citizen"
    OFFICER = "officer"
    ADMIN = "admin"

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    created_at: Optional[datetime] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None