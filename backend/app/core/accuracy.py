import json
import logging
from datetime import date, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

HISTORICAL_PATH = Path(__file__).parent.parent.parent / "data" / "historical_events.json"
ACCURACY_PATH = Path(__file__).parent.parent.parent / "data" / "accuracy.json"


def _load_events() -> list[dict]:
    try:
        with open(HISTORICAL_PATH) as f:
            return json.load(f)
    except Exception:
        return []


def _load_accuracy() -> list[dict]:
    try:
        with open(ACCURACY_PATH) as f:
            return json.load(f)
    except Exception:
        return []


def _save_accuracy(records: list[dict]):
    with open(ACCURACY_PATH, "w") as f:
        json.dump(records, f, indent=2)


def get_nifty_close(date_str: str) -> int | None:
    """Fetch Nifty closing change for a given date from historical events."""
    events = _load_events()
    for e in events:
        if e.get("date") == date_str:
            return e.get("nifty_move")
    return None


def check_yesterday_brief(sentiment: str, date_str: str | None = None) -> dict:
    """Check if yesterday's brief was accurate based on today's knowledge."""
    if date_str is None:
        check_date = (date.today() - timedelta(days=1)).isoformat()
    else:
        check_date = date_str

    accuracy_records = _load_accuracy()

    # Look for existing record
    for r in accuracy_records:
        if r.get("date") == check_date:
            return r

    # Try to check actual move
    actual_move = get_nifty_close(check_date)
    if actual_move is None:
        return {"date": check_date, "predicted": sentiment, "actual_move": None, "correct": None}

    # Determine if prediction was correct
    if sentiment == "neutral":
        correct = abs(actual_move) < 50
    elif sentiment == "bullish":
        correct = actual_move > 0
    else:
        correct = actual_move < 0

    record = {
        "date": check_date,
        "predicted": sentiment,
        "actual_move": actual_move,
        "correct": correct,
    }

    # Update accuracy records
    updated = [r for r in accuracy_records if r.get("date") != check_date]
    updated.append(record)
    _save_accuracy(updated)

    return record


def get_accuracy_stats() -> dict:
    """Get accuracy stats for the last 10, 30, and all days."""
    records = _load_accuracy()

    if not records:
        return {"last_10": 0, "last_30": 0, "total": 0, "count": 0, "recent_days": []}

    # Sort by date descending
    sorted_records = sorted(records, key=lambda r: r.get("date", ""), reverse=True)

    def calc_accuracy(subset: list[dict]) -> tuple[int, int]:
        correct = sum(1 for r in subset if r.get("correct") is True)
        total = sum(1 for r in subset if r.get("correct") is not None)
        return correct, total

    c10, t10 = calc_accuracy(sorted_records[:10])
    c30, t30 = calc_accuracy(sorted_records[:30])
    c_all, t_all = calc_accuracy(sorted_records)

    return {
        "last_10": round(c10 / t10 * 100) if t10 > 0 else 0,
        "last_30": round(c30 / t30 * 100) if t30 > 0 else 0,
        "total": round(c_all / t_all * 100) if t_all > 0 else 0,
        "count": t_all,
        "recent_days": [r for r in sorted_records[:14] if r.get("correct") is not None],
    }
