from pydantic import BaseModel, ConfigDict


class UserProfileResponse(BaseModel):
    id: int
    auth_user_id: int
    full_name: str

    model_config = ConfigDict(from_attributes= True)
    