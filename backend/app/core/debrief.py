import json
import logging
from datetime import date, timedelta, datetime, timezone
from pathlib import Path
from app.services.sentiment import get_overall_sentiment

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


def _get_nifty_move(today: str) -> int | None:
    """Get Nifty closing change for a date from historical events."""
    events = _load_json(HISTORICAL_PATH)
    if isinstance(events, list):
        for e in events:
            if e.get("date") == today:
                return e.get("nifty_move")
    return None


def generate_debrief(manual_date: str = None) -> dict:
    """Generate post-market debrief at 3:30 PM."""
    today = manual_date or date.today().isoformat()

    brief = _load_json(BRIEF_PATH)
    if not isinstance(brief, dict):
        brief = {}

    # Get today's predicted sentiment
    predicted = brief.get("overall_sentiment", "neutral") if brief.get("date") == today else "neutral"

    # Get actual Nifty move
    actual_move = _get_nifty_move(today)

    # Determine if prediction was correct
    if actual_move is not None:
        if predicted == "neutral":
            correct = abs(actual_move) < 50
        elif predicted == "bullish":
            correct = actual_move > 0
        else:
            correct = actual_move < 0

        # Save to accuracy records
        accuracy = _load_json(ACCURACY_PATH)
        if isinstance(accuracy, list):
            updated = [r for r in accuracy if r.get("date") != today]
            updated.append({
                "date": today,
                "predicted": predicted,
                "actual_move": actual_move,
                "correct": correct,
            })
            _save_json(ACCURACY_PATH, updated)
    else:
        correct = None

    # Generate debrief text
    parts = []
    if actual_move is not None:
        direction = "🟢" if actual_move > 0 else "🔴" if actual_move < 0 else "⚪"
        sent_text = "positive" if actual_move > 0 else "negative"
        parts.append(f"Market closed {sent_text} today. Nifty moved {actual_move:+.0f} pts. {direction}")

    if correct is True:
        parts.append("✅ Our pre-market brief called this correctly — we said BULLISH and the market went up.")
    elif correct is False:
        parts.append("⚠️ Our pre-market brief was off today. We predicted {predicted.upper()} but the market moved the other way. This helps us improve.")
    elif correct is None:
        parts.append("📊 Market data for today is still being processed.")

    # Add what to watch tomorrow
    parts.append("🔮 What to watch tomorrow: Key levels to track are support and resistance from today's close. Check tomorrow's brief at 8:45 AM.")

    result = {
        "date": today,
        "predicted": predicted,
        "actual_move": actual_move,
        "correct": correct,
        "debrief_text": " ".join(parts),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    _save_json(DEBRIEF_PATH, result)
    return result
