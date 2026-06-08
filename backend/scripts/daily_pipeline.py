import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path
from app.services.scraper import get_articles
from app.services.sentiment import analyze_batch
from app.core.knowledge_base import enrich_article, detect_event_type
from app.core.fii_scraper import get_fii_data
from app.core.levels import get_key_levels
from app.core.accuracy import check_yesterday_brief, get_accuracy_stats

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
HISTORICAL_PATH = DATA_DIR / "historical_events.json"
BRIEF_PATH = DATA_DIR / "brief.json"
ARTICLES_PATH = DATA_DIR / "articles.json"


def _load_json(path: Path) -> list | dict:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return [] if path.suffix == ".json" and not path.name == "brief.json" else {}


def _save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def run_pipeline():
    logger.info("=" * 50)
    logger.info("  Nifty Brief — Daily Pipeline")
    logger.info(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    logger.info("=" * 50)

    today = date.today().isoformat()

    existing_brief = _load_json(BRIEF_PATH)
    if existing_brief and isinstance(existing_brief, dict) and existing_brief.get("date") == today:
        logger.info("Brief already exists for today — skipping")
        return

    # ── Step 1: Scrape ──────────────────────────────────────────
    logger.info("\nStep 1: Scraping articles...")
    articles = get_articles()
    if not articles:
        logger.error("No articles fetched")
        sys.exit(1)

    # ── Step 2: Sentiment ───────────────────────────────────────
    logger.info(f"\nStep 2: Analyzing {len(articles)} articles...")
    articles = analyze_batch(articles)

    # ── Step 2.5: Enrich with knowledge base ────────────────────
    logger.info("\nStep 2.5: Enriching articles with knowledge base...")
    for article in articles:
        enrich_article(article)

    # ── Step 3: Save articles ───────────────────────────────────
    logger.info(f"\nStep 3: Saving {len(articles)} articles...")
    existing_articles = _load_json(ARTICLES_PATH)
    if isinstance(existing_articles, list):
        existing_articles = existing_articles + articles
        _save_json(ARTICLES_PATH, existing_articles)
    else:
        _save_json(ARTICLES_PATH, articles)

    # ── Step 4: FII data ────────────────────────────────────────
    logger.info("\nStep 4: Fetching FII/DII data...")
    fii_data = get_fii_data()

    # ── Step 5: Detect event type ───────────────────────────────
    logger.info("\nStep 5: Detecting event types...")
    event_types = set()
    for a in articles:
        et = a.get("event_type") or detect_event_type(a.get("title", ""), a.get("body", ""))
        if et:
            event_types.add(et)
    main_event = next(iter(event_types), None)

    # Pick dominant event type (most events in history) for richer context
    try:
        all_hist = _load_json(HISTORICAL_PATH) or []
        if isinstance(all_hist, list):
            type_counts = {}
            for e in all_hist:
                et = e.get("event_type")
                if et:
                    type_counts[et] = type_counts.get(et, 0) + 1
            # Use detected event if it has >= 3 events, else use most common
            if main_event and type_counts.get(main_event, 0) >= 3:
                pass  # keep main_event
            elif type_counts:
                main_event = max(type_counts, key=type_counts.get)
    except Exception:
        pass

    logger.info(f"  Detected: {event_types}, Using: {main_event}")

    # ── Step 6: Key levels ──────────────────────────────────────
    logger.info("\nStep 6: Calculating key levels...")
    key_levels = get_key_levels(main_event)
    logger.info(f"  Support: {key_levels['support']}, Resistance: {key_levels['resistance']}, PCR: {key_levels['pcr']}")

    # ── Step 7: Accuracy check ──────────────────────────────────
    logger.info("\nStep 7: Checking yesterday's accuracy...")
    hist = _load_json(HISTORICAL_PATH)
    sent = "neutral"
    if fii_data.get("fii_index_fut_cr", 0) > 500:
        sent = "bullish"
    elif fii_data.get("fii_index_fut_cr", 0) < -500:
        sent = "bearish"
    # Also check from yesterday's brief sentiment if available
    yesterday = check_yesterday_brief(sent) if existing_brief else {"correct": None}
    accuracy_stats = get_accuracy_stats()

    # ── Step 8: Generate brief ──────────────────────────────────
    logger.info("\nStep 8: Generating brief...")

    # Score articles by importance
    HIGH_IMPACT_KEYWORDS = ["rbi", "repo rate", "cpi", "inflation", "fed", "budget", "fii", "dii", "nifty", "bank nifty", "crash", "surge"]
    for a in articles:
        score = a.get("sentiment_score", 0.5)
        title_lower = a.get("title", "").lower()
        for kw in HIGH_IMPACT_KEYWORDS:
            if kw in title_lower:
                score += 0.15
                break
        if a.get("sentiment_label") in ("bullish", "bearish"):
            score += 0.1
        a["_score"] = score

    top_articles = sorted(articles, key=lambda a: a.get("_score", 0), reverse=True)[:5]
    logger.info(f"  Selected {len(top_articles)} top articles")

    # Calculate overall sentiment
    score_sum = sum(
        a.get("sentiment_score", 0.5) if a.get("sentiment_label") == "bullish"
        else -a.get("sentiment_score", 0.5) if a.get("sentiment_label") == "bearish"
        else 0
        for a in top_articles
    )
    avg_sent = score_sum / len(top_articles) if top_articles else 0
    overall_sent = "bullish" if avg_sent > 0.1 else "bearish" if avg_sent < -0.1 else "neutral"

    # Build summary text
    summary_parts = [f"Market sentiment today is {overall_sent.upper()} based on {len(top_articles)} key articles."]

    # Add historical context if available
    if main_event:
        try:
            hist_events = _load_json(HISTORICAL_PATH)
            relevant = [e for e in (hist_events if isinstance(hist_events, list) else []) if e.get("event_type") == main_event]
            nifty_moves = [e["nifty_move"] for e in relevant if e.get("nifty_move") is not None]
            banknifty_moves = [e["banknifty_move"] for e in relevant if e.get("banknifty_move") is not None]
            if nifty_moves:
                avg_nifty = sum(nifty_moves) / len(nifty_moves)
                direction = "up" if avg_nifty > 0 else "down"
                up = sum(1 for m in nifty_moves if m > 0)
                down = sum(1 for m in nifty_moves if m < 0)
                summary_parts.append(f"Nifty: Last {len(nifty_moves)} {main_event} events {direction} avg {abs(avg_nifty):.0f} pts ({up} up, {down} down).")
            if banknifty_moves:
                avg_bn = sum(banknifty_moves) / len(banknifty_moves)
                direction_bn = "up" if avg_bn > 0 else "down"
                summary_parts.append(f"BankNifty: Last {len(banknifty_moves)} {main_event} events {direction_bn} avg {abs(avg_bn):.0f} pts.")
        except Exception:
            pass

    # Add FII context
    fii_val = fii_data.get("fii_equity_cr", 0) or fii_data.get("fii_index_fut_cr", 0) or 0
    if fii_val != 0:
        fii_dir = "buying" if fii_val > 0 else "selling"
        fii_sent = "positive" if fii_val > 0 else "negative"
        summary_parts.append(f"FIIs are net {fii_dir} ₹{abs(fii_val):,.0f}cr ({fii_sent}).")

    summary_text = " ".join(summary_parts)

    # Build items
    items = []
    for i, a in enumerate(top_articles):
        items.append({
            "id": a.get("id", str(i)),
            "headline": a.get("title", "")[:120],
            "impact_text": f"Sentiment: {a.get('sentiment_label', 'neutral').upper()} with {a.get('sentiment_score', 0.5):.0%} confidence.",
            "sentiment_label": a.get("sentiment_label", "neutral"),
            "sentiment_score": a.get("sentiment_score", 0.5),
            "why": a.get("why", []),
            "sectors": a.get("sectors", {}),
            "stocks": a.get("stocks", []),
            "historical_context": "",
            "source": a.get("source", ""),
            "url": a.get("url", ""),
            "order_index": i,
        })

    # Build historical summaries
    hist_summary_nifty = ""
    hist_summary_banknifty = ""
    if main_event:
        try:
            hist_events = _load_json(HISTORICAL_PATH)
            relevant = [e for e in (hist_events if isinstance(hist_events, list) else []) if e.get("event_type") == main_event]
            nifty_moves = [e["nifty_move"] for e in relevant if e.get("nifty_move") is not None]
            banknifty_moves = [e["banknifty_move"] for e in relevant if e.get("banknifty_move") is not None]

            def summarize(moves, label):
                if not moves:
                    return ""
                avg = sum(moves) / len(moves)
                up = sum(1 for m in moves if m > 0)
                down = sum(1 for m in moves if m < 0)
                direction = "up" if avg > 0 else "down"
                return f"Last {len(moves)} {label} events: {direction} avg {abs(avg):.0f} pts ({up} up, {down} down)"

            hist_summary_nifty = summarize(nifty_moves, main_event)
            hist_summary_banknifty = summarize(banknifty_moves, main_event)

            if items:
                items[0]["historical_context"] = hist_summary_nifty
        except Exception:
            pass

    brief_data = {
        "date": today,
        "overall_sentiment": overall_sent,
        "summary_text": summary_text,
        "items": items,
        "key_levels": key_levels,
        "historical_summary_nifty": hist_summary_nifty,
        "historical_summary_banknifty": hist_summary_banknifty,
        "accuracy": accuracy_stats,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    logger.info(f"  Sentiment: {overall_sent.upper()}")
    logger.info(f"  Summary: {summary_text[:80]}...")

    # ── Step 9: Save brief ──────────────────────────────────────
    logger.info("\nStep 9: Saving brief...")
    _save_json(BRIEF_PATH, brief_data)

    logger.info(f"\n✅ Done! Brief saved for {today}")


if __name__ == "__main__":
    run_pipeline()
