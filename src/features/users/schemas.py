# External imports -----------------------------------------------------------------------------------------------------
from datetime import datetime
from pydantic import BaseModel, EmailStr





# Necessary classes, objects and functions -----------------------------------------------------------------------------

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None





class UserCreate(UserBase):
    password: str





class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}





class UserLogin(BaseModel):
    email: EmailStr
    password: str





class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: EmailStr





class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"





class RefreshRequest(BaseModel):
    refresh_token: str




