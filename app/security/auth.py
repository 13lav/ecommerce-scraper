from fastapi import HTTPException, Request
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="access-token", auto_error=False)


async def match_api_key(request: Request):
    token = request.headers.get("access-token")
    if token == settings.API_KEY:
        return token
    else:
        raise HTTPException(
            status_code=401,  # HTTP 401 Unauthorized
            detail="Invalid or missing API key"
        )
