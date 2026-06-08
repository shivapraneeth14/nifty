import logging
from datetime import date, datetime, timezone
from app.services.sentiment import get_overall_sentiment
from app.services.historical import get_event_summary_index

logger = logging.getLogger(__name__)

TOP_N = 5

HIGH_IMPACT_KEYWORDS = [
    "rbi", "repo rate", "federal reserve", "fed rate",
    "cpi", "inflation", "gdp", "budget", "sebi",
    "nifty", "sensex", "bank nifty", "fii", "dii",
    "earnings", "results", "quarterly",
]


def _score_article(article: dict) -> float:
    score = article.get("sentiment_score", 0.5)
    title_lower = article.get("title", "").lower()
    for kw in HIGH_IMPACT_KEYWORDS:
        if kw in title_lower:
            score += 0.15
            break
    if article.get("sentiment_label") in ("bullish", "bearish"):
        score += 0.1
    return score


def _select_top_articles(articles: list[dict], n: int = TOP_N) -> list[dict]:
    scored = [(a, _score_article(a)) for a in articles]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [a for a, _ in scored[:n]]


def generate_brief(articles: list[dict], historical_events: list[dict] = None) -> dict:
    today = date.today().isoformat()
    historical_events = historical_events or []

    top_articles = _select_top_articles(articles)
    logger.info(f"Selected {len(top_articles)} top articles for brief")

    detected_event_types = set(e["event_type"] for e in historical_events)
    event_type = next(iter(detected_event_types), None)
    hist_summaries = get_event_summary_index(event_type) if event_type else {"nifty": "", "banknifty": ""}

    overall = get_overall_sentiment(top_articles)

    items = []
    for i, a in enumerate(top_articles):
        items.append({
            "headline": a["title"][:100],
            "impact_text": f"Sentiment: {a['sentiment_label'].upper()} with {a['sentiment_score']:.0%} confidence.",
            "sentiment_label": a["sentiment_label"],
            "historical_context": hist_summaries["nifty"] if i == 0 else "",
            "source": a.get("source", ""),
            "url": a.get("url", ""),
            "order_index": i,
        })

    summary_text = f"Market sentiment today is {overall.upper()} based on {len(top_articles)} key articles."
    if hist_summaries["nifty"]:
        summary_text += f" Nifty: {hist_summaries['nifty']}"
    if hist_summaries["banknifty"]:
        summary_text += f" BankNifty: {hist_summaries['banknifty']}"

    return {
        "date": today,
        "overall_sentiment": overall,
        "summary_text": summary_text,
        "items": items,
        "historical_summary_nifty": hist_summaries["nifty"],
        "historical_summary_banknifty": hist_summaries["banknifty"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
