from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenValidationRequest(BaseModel):
    token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenValidationResponse(BaseModel):
    auth_user_id: int
    email: EmailStr
    is_active: bool = True
    created_at: datetime 
    
    model_config = ConfigDict(from_attributes= True)
    
class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes= True)