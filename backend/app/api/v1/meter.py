from fastapi import APIRouter
from app.core.meter import calculate_meter

router = APIRouter(prefix="/meter", tags=["meter"])


@router.get("")
def sentiment_meter(hours: int = 2):
    return calculate_meter(hours)
