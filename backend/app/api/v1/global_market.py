from fastapi import APIRouter
from app.core.global_market import get_global_market_pulse

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/global")
def global_market():
    return get_global_market_pulse()
