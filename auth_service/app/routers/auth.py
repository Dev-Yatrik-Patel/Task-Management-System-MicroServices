from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.responses import success_response, error_response
from app.dependencies.db import get_db
from app.schemas.auth import (
    RegisterRequest, 
    LoginRequest, 
    TokenResponse, 
    TokenValidationRequest, 
    TokenValidationResponse, 
    RegisterResponse )
from app.services.auth_service import (
    register_user,
    authenticate_user,
    validate_token
)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.password)
    data = RegisterResponse.model_validate(user).model_dump(mode="json")
    return success_response(data = data, status_code = status.HTTP_201_CREATED, message = "User registered successfully.")


@router.post("/login")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, payload.email, payload.password)
    token_response_model = TokenResponse(access_token = token)
    data = TokenResponse.model_validate(token_response_model).model_dump(mode="json")
    return success_response(data = data, status_code = status.HTTP_200_OK, message = "User logged-in successfully.")


@router.post("/validate-token")
async def validate(payload: TokenValidationRequest):
    validated_payload = validate_token(payload.token)
    tokenvalidate_response = TokenValidationResponse(auth_user_id= int(validated_payload["sub"])
                                                     ,email= validated_payload["email"]
                                                     ,is_active= bool(validated_payload["is_active"])
                                                     ,created_at= datetime.fromisoformat(validated_payload["created_at"]) )
    data = TokenValidationResponse.model_validate(tokenvalidate_response).model_dump(mode="json")
    return success_response(data = data, status_code = status.HTTP_200_OK, message = "User validated successfully.")