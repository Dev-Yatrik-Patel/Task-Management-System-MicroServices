from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_profile import UserProfile


def get_user_profile(db: Session, auth_user_id: int) -> UserProfile:
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    return profile