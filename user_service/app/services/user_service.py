from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_profile import UserProfile


def get_user_profile(db: Session, current_user: dict) -> UserProfile:
    auth_user_id = current_user["auth_user_id"]
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    return profile

def create_user_profile(db: Session, current_user: dict, profile_name: str) -> UserProfile:
    
    auth_user_id = current_user["auth_user_id"]
    
    existing_profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail="Profile is already been created."
        )
    
    user_profile = UserProfile(auth_user_id = auth_user_id, full_name = profile_name)
    
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    return user_profile

def update_user_profile(db: Session, current_user: dict, profile_name: str) -> UserProfile:
    
    auth_user_id = current_user["auth_user_id"]
    
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    profile.full_name = profile_name
    
    db.commit()
    db.refresh(profile)
    return profile

def delete_user_profile(db: Session, current_user: dict):
    auth_user_id = current_user["auth_user_id"]
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    db.delete(profile)
    db.commit()
    
    return