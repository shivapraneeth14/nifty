from fastapi import APIRouter
from app.core.debrief import generate_debrief
from pathlib import Path
import json

router = APIRouter(prefix="/debrief", tags=["debrief"])

DEBRIEF_PATH = Path(__file__).parent.parent.parent.parent / "data" / "debrief.json"


@router.get("")
def get_debrief():
    try:
        with open(DEBRIEF_PATH) as f:
            return json.load(f)
    except Exception:
        return generate_debrief()
