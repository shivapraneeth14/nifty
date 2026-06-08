from fastapi import APIRouter
from datetime import date
from pathlib import Path
import json

router = APIRouter(prefix="/brief", tags=["brief"])

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
BRIEF_PATH = DATA_DIR / "brief.json"
HISTORICAL_PATH = DATA_DIR / "historical_events.json"


def _summarize_moves(moves: list, label: str) -> str:
    if not moves:
        return ""
    avg = sum(moves) / len(moves)
    up = sum(1 for m in moves if m > 0)
    down = sum(1 for m in moves if m < 0)
    direction = "up" if avg > 0 else "down"
    return f"Last {len(moves)} {label} events: {direction} avg {abs(avg):.0f} pts ({up} times up, {down} times down)"


def _build_index_summaries() -> dict:
    try:
        with open(HISTORICAL_PATH) as f:
            events = json.load(f)
        if not events:
            return {"nifty": "", "banknifty": ""}
        event_types = sorted(set(e["event_type"] for e in events), key=lambda et: sum(1 for e in events if e["event_type"] == et), reverse=True)
        if not event_types:
            return {"nifty": "", "banknifty": ""}
        top_type = event_types[0]
        relevant = [e for e in events if e["event_type"] == top_type]
        nifty = [e["nifty_move"] for e in relevant if e.get("nifty_move") is not None]
        banknifty = [e["banknifty_move"] for e in relevant if e.get("banknifty_move") is not None]
        return {
            "nifty": _summarize_moves(nifty, top_type),
            "banknifty": _summarize_moves(banknifty, top_type),
        }
    except Exception:
        return {"nifty": "", "banknifty": ""}


@router.get("/today")
def get_today_brief():
    today = date.today().isoformat()
    try:
        with open(BRIEF_PATH) as f:
            brief_data = json.load(f)
    except Exception:
        return {"date": today, "overall_sentiment": "neutral", "summary_text": "Brief not yet generated for today.", "items": []}

    if not brief_data or brief_data.get("date") != today:
        return {"date": today, "overall_sentiment": "neutral", "summary_text": "Brief not yet generated for today. Check back around 8:45 AM.", "items": []}

    summaries = _build_index_summaries()
    brief_data["historical_summary_nifty"] = summaries["nifty"]
    brief_data["historical_summary_banknifty"] = summaries["banknifty"]

    return brief_data
