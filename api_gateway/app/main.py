from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.routers import auth, task, user

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(user.router)


@app.exception_handler(HTTPException)
async def app_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "error": {
                "code": "HTTP_ERROR",
                "details": None
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "details": str(exc.errors())
            }
        }
    )
    
@app.get("/")
async def home():
    return {"message": f"Welcome to {settings.APP_NAME}"}

@app.get("/health")
async def health_check():
    return { "message" : f"{settings.APP_NAME} is running!"}