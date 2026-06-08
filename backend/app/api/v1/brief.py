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
    return f"Last {len(moves)} {label} events: {direction} avg {abs(avg):.0f} pts ({up} up, {down} down)"


def _build_index_summaries() -> dict:
    try:
        with open(HISTORICAL_PATH) as f:
            events = json.load(f)
        if not events:
            return {"nifty": "", "banknifty": ""}
        all_types = sorted(set(e["event_type"] for e in events),
                          key=lambda et: sum(1 for e in events if e["event_type"] == et), reverse=True)
        if not all_types:
            return {"nifty": "", "banknifty": ""}
        top = all_types[0]
        rel = [e for e in events if e["event_type"] == top]
        nifty = [e["nifty_move"] for e in rel if e.get("nifty_move") is not None]
        banknifty = [e["banknifty_move"] for e in rel if e.get("banknifty_move") is not None]
        return {
            "nifty": _summarize_moves(nifty, top),
            "banknifty": _summarize_moves(banknifty, top),
        }
    except Exception:
        return {"nifty": "", "banknifty": ""}


def _compute_key_levels(index: str) -> dict:
    try:
        with open(HISTORICAL_PATH) as f:
            events = json.load(f)
    except Exception:
        return {"support": None, "resistance": None}
    if not isinstance(events, list):
        return {"support": None, "resistance": None}
    key = "nifty_move" if index == "nifty" else "banknifty_move"
    moves = [e[key] for e in events if e.get(key) is not None]
    if not moves:
        return {"support": None, "resistance": None}
    positive = [m for m in moves if m > 0]
    negative = [m for m in moves if m < 0]
    support = round(abs(sum(negative) / len(negative)) * 1.1) if negative else None
    resistance = round((sum(positive) / len(positive)) * 1.1) if positive else None
    return {"support": support, "resistance": resistance}


def _load_accuracy() -> dict:
    try:
        acc_path = DATA_DIR / "accuracy.json"
        with open(acc_path) as f:
            acc_records = json.load(f)
        if isinstance(acc_records, list):
            recent = sorted(acc_records, key=lambda r: r.get("date", ""), reverse=True)[:10]
            correct = sum(1 for r in recent if r.get("correct") is True)
            total = sum(1 for r in recent if r.get("correct") is not None)
            return {"recent": round(correct / total * 100) if total > 0 else 0, "total": total, "last_10": f"{correct}/{total}"}
    except Exception:
        pass
    return {"recent": 0, "total": 0, "last_10": "0/0"}


@router.get("/today")
def get_today_brief():
    today = date.today().isoformat()
    try:
        with open(BRIEF_PATH) as f:
            brief_data = json.load(f)
    except Exception:
        return {"date": today,
                "overall_sentiment": "neutral",
                "summary_text": "Brief not yet generated for today.",
                "items": [],
                "sentiment_nifty": "neutral",
                "sentiment_banknifty": "neutral",
                "items_nifty": [],
                "items_banknifty": []}

    if not brief_data or brief_data.get("date") != today:
        return {"date": today, "overall_sentiment": "neutral", "summary_text": "No brief for today yet.",
                "items": [],
                "sentiment_nifty": "neutral", "sentiment_banknifty": "neutral",
                "items_nifty": [], "items_banknifty": []}

    # Add index summary strings
    summaries = _build_index_summaries()
    brief_data["historical_summary_nifty"] = summaries["nifty"]
    brief_data["historical_summary_banknifty"] = summaries["banknifty"]

    # Enrich items with both contexts from the pipeline data
    for item in brief_data.get("items", []):
        item["historical_context_nifty"] = item.get("historical_context_nifty", "")
        item["historical_context_banknifty"] = item.get("historical_context_banknifty", "")

    # Ensure per-index data exists (fallback to defaults if pipeline didn't generate it)
    if "sentiment_nifty" not in brief_data:
        brief_data["sentiment_nifty"] = brief_data.get("overall_sentiment", "neutral")
    if "sentiment_banknifty" not in brief_data:
        brief_data["sentiment_banknifty"] = brief_data.get("overall_sentiment", "neutral")
    if "items_nifty" not in brief_data or not brief_data["items_nifty"]:
        brief_data["items_nifty"] = brief_data.get("items", [])
    if "items_banknifty" not in brief_data or not brief_data["items_banknifty"]:
        brief_data["items_banknifty"] = brief_data.get("items", [])
    if "summary_nifty" not in brief_data:
        brief_data["summary_nifty"] = brief_data.get("summary_text", "")
    if "summary_banknifty" not in brief_data:
        brief_data["summary_banknifty"] = brief_data.get("summary_text", "")
    if "trade_action_nifty" not in brief_data:
        sent_n = brief_data["sentiment_nifty"]
        brief_data["trade_action_nifty"] = f"Nifty sentiment is {sent_n.upper()}."
    if "trade_action_banknifty" not in brief_data:
        sent_b = brief_data["sentiment_banknifty"]
        brief_data["trade_action_banknifty"] = f"BankNifty sentiment is {sent_b.upper()}."

    # Index-specific key levels
    brief_data["key_levels_nifty"] = _compute_key_levels("nifty")
    brief_data["key_levels_banknifty"] = _compute_key_levels("banknifty")

    # Accuracy
    brief_data["accuracy"] = _load_accuracy()

    return brief_data
