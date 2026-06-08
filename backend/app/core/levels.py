import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

HISTORICAL_PATH = Path(__file__).parent.parent.parent / "data" / "historical_events.json"


def _load_events() -> list[dict]:
    try:
        with open(HISTORICAL_PATH) as f:
            return json.load(f)
    except Exception:
        return []


def calculate_support_resistance(event_type: str | None = None) -> dict:
    """Calculate support and resistance levels based on historical events.

    Support: average of negative moves + 10% buffer
    Resistance: average of positive moves + 10% buffer
    """
    events = _load_events()

    if event_type:
        filtered = [e for e in events if e.get("event_type") == event_type]
    else:
        filtered = events

    nifty_moves = [e["nifty_move"] for e in filtered if e.get("nifty_move") is not None]

    if not nifty_moves:
        return {"support": None, "resistance": None}

    positive = [m for m in nifty_moves if m > 0]
    negative = [m for m in nifty_moves if m < 0]

    support = round(abs(sum(negative) / len(negative)) * 1.1) if negative else None
    resistance = round((sum(positive) / len(positive)) * 1.1) if positive else None

    return {"support": support, "resistance": resistance}


def get_pcr_from_nifty(event_type: str | None = None) -> float | None:
    """Simplified PCR estimate based on event sentiment history."""
    events = _load_events()
    if event_type:
        filtered = [e for e in events if e.get("event_type") == event_type]
    else:
        filtered = events

    bullish = sum(1 for e in filtered if e.get("sentiment_after") == "bullish")
    bearish = sum(1 for e in filtered if e.get("sentiment_after") == "bearish")

    if bearish == 0:
        return 1.5

    ratio = round(bullish / bearish, 2) if bearish > 0 else 1.5
    return min(max(ratio, 0.3), 3.0)


def get_key_levels(event_type: str | None = None) -> dict:
    """Get support, resistance, and PCR for the given event type.
    Falls back to all events if specific type has too few entries."""
    levels = calculate_support_resistance(event_type)
    # If too few events for specific type, fall back to all events
    if event_type:
        all_events = _load_events()
        specific = [e for e in all_events if e.get("event_type") == event_type]
        if len(specific) < 3:
            levels = calculate_support_resistance(None)
            pcr = get_pcr_from_nifty(None)
        else:
            pcr = get_pcr_from_nifty(event_type)
    else:
        pcr = get_pcr_from_nifty(None)

    # Get FII data
    fii_cr = 0
    try:
        from app.core.fii_scraper import FII_DATA_PATH
        import json
        with open(FII_DATA_PATH) as f:
            fii_data = json.load(f)
            fii_cr = fii_data.get("fii_equity_cr", 0) or fii_data.get("fii_index_fut_cr", 0) or 0
    except Exception:
        pass

    return {
        "support": levels["support"],
        "resistance": levels["resistance"],
        "pcr": pcr,
        "fii_cr": fii_cr,
    }
