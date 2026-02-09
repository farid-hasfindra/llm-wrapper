from fastapi import APIRouter, Depends
from app.core.security import get_api_key

router = APIRouter()

@router.get("/stats", dependencies=[Depends(get_api_key)])
async def get_stats():
    """
    Get system statistics (Mocked for portfolio).
    """
    return {
        "requests_processed": 100,
        "average_latency_ms": 150,
        "tokens_generated": 5000
    }
