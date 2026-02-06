from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.responses import success_response, error_response
from app.dependencies.db import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, TokenValidationRequest, TokenValidationResponse
from app.services.auth_service import (
    register_user,
    authenticate_user,
    validate_token
)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.password)
    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, payload.email, payload.password)
    return {"access_token": token}


@router.post("/validate-token", response_model=TokenValidationResponse)
async def validate(payload: TokenValidationRequest):
    data = validate_token(payload.token)
    return {
        "user_id": int(data["sub"]),
        "email": data["email"],
    }