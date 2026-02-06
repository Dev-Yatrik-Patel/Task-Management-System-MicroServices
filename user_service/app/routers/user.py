from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.services.user_service import get_user_profile
from app.schemas.user import UserProfileResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def read_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_profile(db, current_user["data"]["auth_user_id"])