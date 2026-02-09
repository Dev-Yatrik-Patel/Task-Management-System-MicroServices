import json
import httpx
from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.redis import redis_client
from redis.exceptions import ConnectionError

security = HTTPBearer()

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    
    token = authorization.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    # try redis first
    redis_key = f"auth:token:{token}"
    
    try: 
        cached_user = await redis_client.get(redis_key)
    except (ConnectionError, ConnectionRefusedError):
        # Fallback to the Auth Service if Redis is down
        cached_user = None
    
    if cached_user:
        return json.loads(cached_user)

    # fallback auth service call
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTH_SERVICE_URL}/auth/validate-token",
                json={"token": token},
                timeout=5
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Auth service unavailable"
            )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_data = response.json()["data"]
    
    # cached user data 
    expires_in = response.json().get("expires_in", 900)
    
    await redis_client.set(redis_key, json.dumps(user_data), ex=expires_in)
    
    return user_data