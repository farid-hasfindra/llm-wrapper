from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validates API key from request header.
    In a real scenario, this would check against a database of valid keys.
    For this portfolio, we might just allow a 'demo-key' or similar.
    """
    if not api_key_header:
         # For open portfolio, maybe allow without key or enforce a simple one
         # raise HTTPException(
         #    status_code=status.HTTP_403_FORBIDDEN,
         #    detail="Could not validate credentials",
         # )
         return None
    
    # Mock validation
    if api_key_header != "demo-key":
        # raise HTTPException(
        #    status_code=status.HTTP_403_FORBIDDEN,
        #    detail="Invalid API Key",
        # )
        pass
        
    return api_key_header
