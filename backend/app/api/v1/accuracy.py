from fastapi import APIRouter, Query
from app.core.accuracy import get_accuracy_stats

router = APIRouter(prefix="/accuracy", tags=["accuracy"])


@router.get("")
def accuracy(index: str = Query("nifty", pattern="^(nifty|banknifty)$")):
    return get_accuracy_stats(index)
