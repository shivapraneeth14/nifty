import logging
from app.database import supabase

logger = logging.getLogger(__name__)

EVENT_KEYWORDS = {
    "RBI": ["rbi", "repo rate", "monetary policy", "mpc", "rbi governor"],
    "FED": ["federal reserve", "fed rate", "fomc", "powell", "us fed"],
    "CPI": ["cpi", "inflation", "consumer price", "wpi", "retail inflation"],
    "BUDGET": ["budget", "fiscal deficit", "finance minister", "nirmala"],
    "GDP": ["gdp", "gross domestic product", "economic growth"],
    "EARNINGS": ["quarterly results", "q1 results", "earnings"],
    "GLOBAL": ["global sell-off", "geopolitical", "crude oil", "dollar index"],
}


def _detect_event_types(articles: list[dict]) -> list[str]:
    detected = set()
    for article in articles:
        text = f"{article.get('title', '').lower()} {article.get('body', '').lower()[:500]}"
        for event_type, keywords in EVENT_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                detected.add(event_type)
    return list(detected)


def get_relevant_history(articles: list[dict], limit_per_type: int = 5) -> list[dict]:
    event_types = _detect_event_types(articles)
    if not event_types:
        return []

    all_events = []
    for event_type in event_types:
        try:
            result = (
                supabase.table("historical_events")
                .select("*")
                .eq("event_type", event_type)
                .order("date", desc=True)
                .limit(limit_per_type)
                .execute()
            )
            if result.data:
                all_events.extend(result.data)
        except Exception as e:
            logger.error(f"Error querying history for {event_type}: {e}")
    return all_events


def get_event_summary(event_type: str) -> str:
    try:
        result = (
            supabase.table("historical_events")
            .select("nifty_move, banknifty_move, date")
            .eq("event_type", event_type)
            .order("date", desc=True)
            .limit(8)
            .execute()
        )
        events = result.data or []
    except Exception:
        return ""

    if not events:
        return ""

    moves = [e["nifty_move"] for e in events if e.get("nifty_move") is not None]
    if not moves:
        return ""

    avg_move = sum(moves) / len(moves)
    up_count = sum(1 for m in moves if m > 0)
    down_count = sum(1 for m in moves if m < 0)
    direction = "up" if avg_move > 0 else "down"

    return (
        f"Last {len(moves)} {event_type} events: "
        f"Nifty {direction} avg {abs(avg_move):.0f} pts "
        f"({up_count} times up, {down_count} times down)"
    )
