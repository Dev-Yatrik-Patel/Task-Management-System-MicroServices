import httpx
from fastapi import APIRouter, Request, HTTPException, status, Response

from app.core.config import settings

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def task_proxy(path: str, request: Request):
    
    # Read body once
    body = await request.body()
    
    # Remove host header (very important for proxies)
    headers = dict(request.headers)
    headers.pop("host", None)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method = request.method,
                url = f"{settings.TASK_SERVICE_URL}/tasks/{path}",
                headers = headers,
                content = body,
                params = request.query_params,
                timeout = 5
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Task service unavailable",
            )

    if response.status_code == 204:
        return None

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
    )