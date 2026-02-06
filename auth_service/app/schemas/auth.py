from pydantic import BaseModel, EmailStr, ConfigDict

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
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes= True)
    
class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes= True)