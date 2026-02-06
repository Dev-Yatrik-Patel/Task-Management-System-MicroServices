from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.services.user_service import get_user_profile, create_user_profile, update_user_profile, delete_user_profile
from app.schemas.user import UserProfileRequest, UserProfileResponse, UserProfileUpdateRequest

from app.core.responses import success_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def read_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_profile = get_user_profile(db = db, current_user = current_user)
    return success_response( data = UserProfileResponse.model_validate(user_profile).model_dump(mode="json")
                            , message = "Profile fetched successfully", status_code = status.HTTP_200_OK)

@router.post("/createprofile")
async def create_profile(
    userprofile_request_payload : UserProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    created_profile = create_user_profile(db = db, current_user = current_user, profile_name = userprofile_request_payload.full_name)
    return success_response( data = UserProfileResponse.model_validate(created_profile).model_dump(mode="json")
                            , message = "Profile created successfully.", status_code = status.HTTP_201_CREATED)


@router.put("/updateprofile")
async def update_profile(
    userprofile_update_payload : UserProfileUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated_profile = update_user_profile(db = db, current_user = current_user, profile_name = userprofile_update_payload.full_name)
    return success_response( data = UserProfileResponse.model_validate(updated_profile).model_dump(mode="json")
                            , message = "Profile updated successfully.", status_code = status.HTTP_200_OK)

@router.delete("/deleteprofile")
async def delete_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_user_profile(db = db, current_user = current_user)
    return success_response( message = "Profile deleted successfully.", status_code = status.HTTP_200_OK)