from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError

from app.core.responses import error_response
from app.core.config import settings
from app.routers import user

app = FastAPI(title=settings.APP_NAME)

app.include_router(user.router)

@app.exception_handler(HTTPException)
async def app_exception_handler(request: Request, exc: HTTPException):
    return error_response(
        message=exc.detail,
        error_code="HTTP_ERROR",
        status_code=exc.status_code
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        message="Validation error",
        error_code="VALIDATION_ERROR",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=str(exc.errors())
    )

@app.get("/")
async def home():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get("/health")
async def health_check():
    return { "message" : f"{settings.APP_NAME} is running!"}