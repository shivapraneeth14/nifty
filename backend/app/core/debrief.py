import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

BRIEF_PATH = Path(__file__).parent.parent.parent / "data" / "brief.json"
HISTORICAL_PATH = Path(__file__).parent.parent.parent / "data" / "historical_events.json"
DEBRIEF_PATH = Path(__file__).parent.parent.parent / "data" / "debrief.json"
ACCURACY_PATH = Path(__file__).parent.parent.parent / "data" / "accuracy.json"


def _load_json(path: Path) -> dict | list:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _check_one(predicted: str, actual: int | None) -> bool | None:
    if actual is None:
        return None
    if predicted == "neutral":
        return abs(actual) < 50
    elif predicted == "bullish":
        return actual > 0
    else:
        return actual < 0


def generate_debrief(manual_date: str = None) -> dict:
    """Generate post-market debrief checking both indices."""
    today = manual_date or date.today().isoformat()

    brief = _load_json(BRIEF_PATH)
    if not isinstance(brief, dict):
        brief = {}

    is_today = brief.get("date") == today
    pred_nifty = brief.get("sentiment_nifty", "neutral") if is_today else "neutral"
    pred_bn = brief.get("sentiment_banknifty", "neutral") if is_today else "neutral"

    events = _load_json(HISTORICAL_PATH)
    if isinstance(events, list):
        nifty_move = None
        banknifty_move = None
        for e in events:
            if e.get("date") == today:
                nifty_move = e.get("nifty_move")
                banknifty_move = e.get("banknifty_move")
                break
    else:
        nifty_move = None
        banknifty_move = None

    nifty_correct = _check_one(pred_nifty, nifty_move)
    bn_correct = _check_one(pred_bn, banknifty_move)

    accuracy = _load_json(ACCURACY_PATH)
    if isinstance(accuracy, list):
        updated = [r for r in accuracy if r.get("date") != today]
        updated.append({
            "date": today,
            "predicted_nifty": pred_nifty,
            "nifty_move": nifty_move,
            "nifty_correct": nifty_correct,
            "predicted_banknifty": pred_bn,
            "banknifty_move": banknifty_move,
            "banknifty_correct": bn_correct,
        })
        _save_json(ACCURACY_PATH, updated)

    parts = []
    if nifty_move is not None:
        dir_n = "positive" if nifty_move > 0 else "negative"
        parts.append(f"Nifty closed {dir_n} at {nifty_move:+.0f} pts.")
        if nifty_correct is True:
            parts.append("✅ Nifty call was CORRECT.")
        elif nifty_correct is False:
            parts.append("⚠️ Nifty call was off today.")
    if banknifty_move is not None:
        dir_b = "positive" if banknifty_move > 0 else "negative"
        parts.append(f"BankNifty closed {dir_b} at {banknifty_move:+.0f} pts.")
        if bn_correct is True:
            parts.append("✅ BankNifty call was CORRECT.")
        elif bn_correct is False:
            parts.append("⚠️ BankNifty call was off today.")

    result = {
        "date": today,
        "predicted_nifty": pred_nifty,
        "nifty_move": nifty_move,
        "nifty_correct": nifty_correct,
        "predicted_banknifty": pred_bn,
        "banknifty_move": banknifty_move,
        "banknifty_correct": bn_correct,
        "debrief_text": " ".join(parts) if parts else "No data available for today.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    _save_json(DEBRIEF_PATH, result)
    return result
