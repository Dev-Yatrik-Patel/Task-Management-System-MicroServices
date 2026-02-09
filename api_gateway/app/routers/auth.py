import httpx
from fastapi import APIRouter, Request, HTTPException, status, Response

from app.core.config import settings

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

# `path` -> variable name
# * `:path` -> FastAPI / Starlette path converter

# All of these will hit the same function:
# /auth/register
# /auth/login
# /auth/validate-token
# /auth/anything/else/here

# And inside the function:

# path == "register"
# path == "login"
# path == "validate-token"
# path == "anything/else/here"

@router.api_route("/{path:path}", methods = ["POST"])
async def auth_proxy(path: str, request: Request):
    
    # Read body once
    body = await request.body()
    
    # Remove host header (very important for proxies)
    headers = dict[str, str](request.headers)
    headers.pop("host", None)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method = request.method,
                url = f"{settings.AUTH_SERVICE_URL}/auth/{path}",
                headers = headers,
                content = body,
                params = request.query_params,
                timeout = 5
            )
        except httpx.RequestError as e: 
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail = "Auth Service Unavailable")
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )
