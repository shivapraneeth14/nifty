import logging
import re
import time

logger = logging.getLogger(__name__)

BULLISH_WORDS = {
    "surges", "surge", "gains", "gain", "rally", "rallies", "bullish",
    "positive", "growth", "rise", "rises", "record", "high", "higher",
    "up", "upward", "outperform", "beat", "beats", "exceed", "exceeds",
    "strong", "strength", "recovery", "rebound", "boom", "expansion",
    "profit", "profits", "upgrade", "upgraded", "buy", "recommend",
    "optimistic", "confidence", "improve", "improves", "improved",
    "breakout", "support", " recovered", "rebounds", "gains",
    "green", "upbeat", "soars", "soared", "jump", "jumps", "jumped",
    "climb", "climbs", "climbed", "spike", "spikes", "spiked",
    "fair", "attractive", "overweight", "accumulate", "buying",
}

BEARISH_WORDS = {
    "crashes", "crash", "falls", "fall", "falling", "loss", "losses",
    "bearish", "negative", "decline", "declines", "down", "downward",
    "slump", "slumps", "plunge", "plunges", "bear", "bear market",
    "sell-off", "selloff", "drop", "drops", "dropped", "lower",
    "weak", "weakness", "slowdown", "slow", "downgrade", "downgraded",
    "sell", "underperform", "below", "miss", "misses", "cut", "cuts",
    "fear", "panic", "uncertainty", "volatility", "risk", "risks",
    "bearish", "pessimistic", "worse", "worst", "declining",
    "red", "sliding", "slid", "tumble", "tumbles", "tumbled",
    "retreat", "retreats", "retreated", "sink", "sinks", "sank",
    "underweight", "reduce", "bears", "bearish", "stress",
    "subdued", "bleak", "sluggish", "dismal", "gloomy",
}

NEUTRAL_WORDS = {
    "holds", "hold", "unchanged", "steady", "stable", "flat",
    "mixed", "range-bound", "consolidate", "consolidation",
    "wait", "awaits", "expected", "anticipate", "anticipated",
    "neutral", "moderate", "balanced", "steady",
}


def _keyword_sentiment(title: str, body: str = "") -> dict:
    """Simple keyword-based sentiment as fallback when HF API is unavailable."""
    text = f"{title} {body}".lower()

    bullish_count = sum(1 for w in BULLISH_WORDS if w in text)
    bearish_count = sum(1 for w in BEARISH_WORDS if w in text)
    neutral_count = sum(1 for w in NEUTRAL_WORDS if w in text)

    total = bullish_count + bearish_count + neutral_count

    if total == 0:
        return {"label": "neutral", "score": 0.5}

    max_count = max(bullish_count, bearish_count, neutral_count)

    if bullish_count == max_count and bullish_count > bearish_count:
        score = min(0.5 + (bullish_count / total) * 0.4, 0.95)
        return {"label": "bullish", "score": round(score, 4)}
    elif bearish_count == max_count and bearish_count > bullish_count:
        score = min(0.5 + (bearish_count / total) * 0.4, 0.95)
        return {"label": "bearish", "score": round(score, 4)}
    else:
        return {"label": "neutral", "score": 0.5}


def _try_hf_api(title: str, body: str = "") -> dict | None:
    """Try HuggingFace FinBERT API. Returns None on failure."""
    try:
        from huggingface_hub import InferenceClient
        from app.config import settings

        client = InferenceClient(token=settings.hf_api_token)

        text = f"{title}. {body[:300]}" if body else title
        result = client.text_classification(
            text[:512],
            model="ProsusAI/finbert",
        )

        if result:
            best = max(result, key=lambda x: x.score)
            label_map = {
                "positive": "bullish", "negative": "bearish", "neutral": "neutral",
                "POSITIVE": "bullish", "NEGATIVE": "bearish", "NEUTRAL": "neutral",
                "LABEL_0": "bearish", "LABEL_1": "neutral", "LABEL_2": "bullish",
            }
            return {
                "label": label_map.get(best.label, "neutral"),
                "score": round(best.score, 4),
            }
    except Exception as e:
        logger.warning(f"HF API unavailable, using keyword fallback: {str(e)[:80]}")
        return None

    return None


def analyze_article(title: str, body: str = "") -> dict:
    """Try HF API first, fall back to keyword-based sentiment."""
    result = _try_hf_api(title, body)
    if result:
        return result

    return _keyword_sentiment(title, body)


def analyze_batch(articles: list[dict]) -> list[dict]:
    for i, article in enumerate(articles):
        sentiment = analyze_article(
            title=article.get("title", ""),
            body=article.get("body", ""),
        )
        article["sentiment_label"] = sentiment["label"]
        article["sentiment_score"] = sentiment["score"]
        logger.info(
            f"  [{i+1}/{len(articles)}] {sentiment['label'].upper()} ({sentiment['score']:.2f}) "
            f"— {article['title'][:60]}"
        )
        if i < len(articles) - 1:
            time.sleep(0.3)
    return articles


def get_overall_sentiment(articles: list[dict]) -> str:
    if not articles:
        return "neutral"
    score_sum = 0.0
    for a in articles:
        label = a.get("sentiment_label", "neutral")
        score = a.get("sentiment_score", 0.5)
        if label == "bullish":
            score_sum += score
        elif label == "bearish":
            score_sum -= score
    avg = score_sum / len(articles)
    if avg > 0.1:
        return "bullish"
    elif avg < -0.1:
        return "bearish"
    return "neutral"
