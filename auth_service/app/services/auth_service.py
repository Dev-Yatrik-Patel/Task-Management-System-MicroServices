from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)

class AuthService:
    
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, email: str, password: str) -> User:
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = User(
            email=email,
            password_hash=hash_password(password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "is_active" : str(user.is_active), "created_at": str(user.created_at)}
        )
        return token
    
    @staticmethod
    def validate_token(token: str) -> dict:
        try:
            payload = decode_token(token)
            return payload
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )