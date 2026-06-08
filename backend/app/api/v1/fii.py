from fastapi import APIRouter
from app.core.fii_scraper import get_fii_data

router = APIRouter(prefix="/fii", tags=["fii"])


@router.get("")
def fii_data():
    return get_fii_data()
