from app.services.sentiment import get_overall_sentiment
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

ARTICLES_PATH = Path(__file__).parent.parent.parent / "data" / "articles.json"
METER_PATH = Path(__file__).parent.parent.parent / "data" / "meter.json"


def _load_articles() -> list[dict]:
    try:
        with open(ARTICLES_PATH) as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def calculate_meter(hours: int = 2) -> dict:
    """Calculate live sentiment meter based on recent articles.

    Returns a score from -1 (extremely bearish) to +1 (extremely bullish)
    with breakdown by index.
    """
    all_articles = _load_articles()
    if not all_articles:
        return {"nifty": 0, "banknifty": 0, "overall": "neutral", "article_count": 0}

    # Filter by recency
    now = datetime.now(timezone.utc)
    recent = []
    for a in all_articles:
        try:
            pub = a.get("published_at", "")
            if pub:
                pub_time = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                if (now - pub_time).total_seconds() < hours * 3600:
                    recent.append(a)
        except Exception:
            recent.append(a)

    if not recent:
        recent = all_articles[-20:]  # fallback: last 20 articles

    # Calculate scores
    nifty_scores = []
    banknifty_scores = []
    for a in recent:
        label = a.get("sentiment_label", "neutral")
        score = a.get("sentiment_score", 0.5)
        signed_score = score if label == "bullish" else -score if label == "bearish" else 0

        title = (a.get("title", "") + " " + (a.get("body", "") or "")).lower()
        if "nifty" in title or "sensex" in title or "index" in title:
            nifty_scores.append(signed_score)
        if "bank" in title or "banknifty" in title or "pnb" in title or "sbi" in title:
            banknifty_scores.append(signed_score)

        if not nifty_scores:
            nifty_scores.append(signed_score)
        if not banknifty_scores:
            banknifty_scores.append(signed_score)

    nifty_val = round(sum(nifty_scores) / len(nifty_scores), 3) if nifty_scores else 0
    banknifty_val = round(sum(banknifty_scores) / len(banknifty_scores), 3) if banknifty_scores else 0

    def to_label(val):
        return "bullish" if val > 0.1 else "bearish" if val < -0.1 else "neutral"

    result = {
        "nifty": nifty_val,
        "banknifty": banknifty_val,
        "overall": to_label((nifty_val + banknifty_val) / 2),
        "article_count": len(recent),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        with open(METER_PATH, "w") as f:
            json.dump(result, f, indent=2)
    except Exception:
        pass

    return result
