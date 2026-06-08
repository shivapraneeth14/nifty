import json
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent / "data" / "knowledge_base.json"

MODIFIER_KEYWORDS = {
    "hold": ["hold", "holds", "unchanged", "kept", "maintained", "steady", "status quo", "no change"],
    "cut": ["cut", "cuts", "cutting", "reduce", "reduces", "reduction", "lower", "ease", "easing", "decrease"],
    "hike": ["hike", "hikes", "hiked", "raise", "raises", "raised", "increase", "increases", "increased", "tighten"],
    "above_estimate": ["above estimate", "higher than", "exceeds", "surprises on the upside", "hotter than", "beat estimate", "beats estimate"],
    "below_estimate": ["below estimate", "lower than", "misses", "softer than", "cooler than", "miss estimate"],
    "capex_focus": ["capex", "infrastructure", "capital expenditure", "road", "railway", "highway", "bridge"],
    "populist": ["rural", "farmer", "subsidy", "free scheme", "pm kisan", "direct benefit", "dbt"],
    "fiscal_consolidation": ["fiscal deficit", "fiscal consolidation", "fiscal discipline", "fiscal target"],
    "beat": ["beat estimate", "beats estimate", "above estimate", "better than expected", "record profit", "strong result"],
    "miss": ["miss estimate", "misses estimate", "below estimate", "worse than expected", "profit fall", "loss", "weak result"],
    "selloff": ["sell-off", "selloff", "crash", "crashes", "plunge", "plunges", "meltdown", "bloodbath", "global sell"],
    "geopolitical": ["war", "conflict", "geopolitical", "tension", "invasion", "sanction", "military", "strike"],
    "oil_spike": ["crude", "oil price", "oil spike", "oil surge", "petrol", "brent", "wti"],
}

EVENT_TYPE_KEYWORDS = {
    "RBI": ["rbi", "repo rate", "monetary policy", "mpc", "rbi governor", "dash", "shaktikanta"],
    "FED": ["federal reserve", "fed rate", "fomc", "powell", "us fed", "jerome powell"],
    "CPI": ["cpi", "inflation", "consumer price", "retail inflation", "wpi"],
    "BUDGET": ["budget", "union budget", "finance minister", "nirmala sitharaman", "budget 202"],
    "GDP": ["gdp", "gross domestic product", "economic growth", "q1 gdp", "q2 gdp"],
    "EARNINGS": ["quarterly results", "q1 results", "q2 results", "q3 results", "q4 results", "earnings", "net profit", "revenue growth"],
    "GLOBAL": ["global sell-off", "geopolitical", "crude oil", "dollar index", "us market", "wall street", "global market"],
}


def load_knowledge_base() -> dict:
    try:
        with open(KNOWLEDGE_BASE_PATH) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load knowledge base: {e}")
        return {}


def detect_event_type(title: str, body: str = "") -> str | None:
    text = f"{title} {body}".lower()
    for event_type, keywords in EVENT_TYPE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return event_type
    return None


def detect_modifier(title: str, body: str = "") -> str | None:
    text = f"{title} {body}".lower()
    for modifier, keywords in MODIFIER_KEYWORDS.items():
        if any(re.search(rf'\b{kw}\b', text) for kw in keywords):
            return modifier
    return None


def get_explanation(event_type: str, modifier: str) -> dict | None:
    kb = load_knowledge_base()
    event_data = kb.get(event_type)
    if not event_data:
        return None
    modifier_data = event_data.get("modifiers", {}).get(modifier)
    if not modifier_data:
        return None
    return modifier_data


def enrich_article(article: dict) -> dict:
    """Add why/sectors/stocks to an article based on detected event type + modifier."""
    title = article.get("title", "")
    body = article.get("body", "")

    event_type = detect_event_type(title, body)
    modifier = detect_modifier(title, body)

    article["event_type"] = event_type
    article["event_modifier"] = modifier

    if event_type and modifier:
        explanation = get_explanation(event_type, modifier)
        if explanation:
            article["why"] = explanation.get("chain", [])
            article["sectors"] = explanation.get("sectors", {})
            article["stocks"] = explanation.get("stocks", [])
        else:
            article["why"] = []
            article["sectors"] = {}
            article["stocks"] = []
    else:
        article["why"] = []
        article["sectors"] = {}
        article["stocks"] = []

    return article
