from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ========== АУТЕНТИФИКАЦИЯ ==========
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None

# ========== ВЫПУСКНИКИ ==========
class GraduateBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    specialty_id: Optional[int] = None
    graduation_year_id: Optional[int] = None

class GraduateCreate(GraduateBase):
    pass

class GraduateResponse(GraduateBase):
    id: int
    user_id: Optional[int] = None
    is_employed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True