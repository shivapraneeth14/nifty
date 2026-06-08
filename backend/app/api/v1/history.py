from fastapi import APIRouter, Query
from pathlib import Path
import json

router = APIRouter(prefix="/history", tags=["history"])

HISTORICAL_PATH = Path(__file__).parent.parent.parent.parent / "data" / "historical_events.json"


@router.get("")
def get_history(event_type: str = Query(None), limit: int = Query(50, le=100)):
    try:
        with open(HISTORICAL_PATH) as f:
            events = json.load(f)
    except Exception:
        return {"events": []}

    if not isinstance(events, list):
        return {"events": []}

    if event_type:
        events = [e for e in events if e.get("event_type", "").upper() == event_type.upper()]

    events.sort(key=lambda e: e.get("date", ""), reverse=True)

    return {"events": events[:limit]}
