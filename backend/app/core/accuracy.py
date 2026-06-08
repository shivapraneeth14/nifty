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


def get_index_close(date_str: str, index: str = "nifty") -> int | None:
    """Get closing change for a specific index from historical events."""
    key = "nifty_move" if index == "nifty" else "banknifty_move"
    events = _load_events()
    for e in events:
        if e.get("date") == date_str:
            return e.get(key)
    return None


def _check_one(predicted: str, actual: int | None) -> bool | None:
    """Check if a prediction was correct for a single index."""
    if actual is None:
        return None
    if predicted == "neutral":
        return abs(actual) < 50
    elif predicted == "bullish":
        return actual > 0
    else:
        return actual < 0


def check_yesterday_brief(predicted_nifty: str, predicted_banknifty: str, date_str: str | None = None) -> dict:
    """Check yesterday's brief accuracy for both indices."""
    if date_str is None:
        check_date = (date.today() - timedelta(days=1)).isoformat()
    else:
        check_date = date_str

    records = _load_accuracy()
    for r in records:
        if r.get("date") == check_date:
            return r

    nifty_move = get_index_close(check_date, "nifty")
    banknifty_move = get_index_close(check_date, "banknifty")

    record = {
        "date": check_date,
        "predicted_nifty": predicted_nifty,
        "nifty_move": nifty_move,
        "nifty_correct": _check_one(predicted_nifty, nifty_move),
        "predicted_banknifty": predicted_banknifty,
        "banknifty_move": banknifty_move,
        "banknifty_correct": _check_one(predicted_banknifty, banknifty_move),
    }

    updated = [r for r in records if r.get("date") != check_date]
    updated.append(record)
    _save_accuracy(updated)

    return record


def get_accuracy_stats(index: str = "nifty") -> dict:
    """Get accuracy stats for a specific index."""
    records = _load_accuracy()
    if not records:
        return {"last_10": 0, "last_30": 0, "total": 0, "count": 0, "recent_days": []}

    sorted_records = sorted(records, key=lambda r: r.get("date", ""), reverse=True)

    correct_key = f"{index}_correct"
    move_key = f"{index}_move"

    def calc_accuracy(subset: list[dict]) -> tuple[int, int]:
        correct = sum(1 for r in subset if r.get(correct_key) is True)
        total = sum(1 for r in subset if r.get(correct_key) is not None)
        return correct, total

    c10, t10 = calc_accuracy(sorted_records[:10])
    c30, t30 = calc_accuracy(sorted_records[:30])
    c_all, t_all = calc_accuracy(sorted_records)

    recent = []
    for r in sorted_records[:14]:
        if r.get(correct_key) is not None:
            recent.append({
                "date": r.get("date", ""),
                "predicted": r.get(f"predicted_{index}", ""),
                "actual_move": r.get(move_key),
                "correct": r.get(correct_key),
            })

    return {
        "last_10": round(c10 / t10 * 100) if t10 > 0 else 0,
        "last_30": round(c30 / t30 * 100) if t30 > 0 else 0,
        "total": round(c_all / t_all * 100) if t_all > 0 else 0,
        "count": t_all,
        "recent_days": recent,
    }
