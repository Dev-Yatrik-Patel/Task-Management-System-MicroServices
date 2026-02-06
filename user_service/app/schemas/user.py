from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserProfileRequest(BaseModel):
    full_name: str
    
class UserProfileUpdateRequest(BaseModel):
    full_name: str

class UserProfileResponse(BaseModel):
    id: int
    auth_user_id: int
    full_name: str
    created_at : datetime

    model_config = ConfigDict(from_attributes= True)