from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_profile import UserProfile


class UserProfileService:
    
    def __init__(self, db:Session, current_user: dict):
        self.db = db
        self.current_user = current_user
        self.auth_user_id = self.current_user["auth_user_id"]
    
    def get_user_profile(self) -> UserProfile:
        
        profile = self.db.query(UserProfile).filter(
            UserProfile.auth_user_id == self.auth_user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        return profile

    def create_user_profile(self, profile_name: str) -> UserProfile:
        
        existing_profile = self.db.query(UserProfile).filter(
            UserProfile.auth_user_id == self.auth_user_id
        ).first()
        
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Profile is already been created."
            )
        
        user_profile = UserProfile(auth_user_id = self.auth_user_id, full_name = profile_name)
        
        self.db.add(user_profile)
        self.db.commit()
        self.db.refresh(user_profile)
        return user_profile

    def update_user_profile(self, profile_name: str) -> UserProfile:
        
        profile = self.db.query(UserProfile).filter(
            UserProfile.auth_user_id == self.auth_user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile.full_name = profile_name
        
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete_user_profile(self):
        
        profile = self.db.query(UserProfile).filter(
            UserProfile.auth_user_id == self.auth_user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        self.db.delete(profile)
        self.db.commit()
        
        return