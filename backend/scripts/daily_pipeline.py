import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path
from app.services.scraper import get_articles
from app.services.sentiment import analyze_batch, get_index_sentiments
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
    logger.info("\nStep 8: Generating brief with per-index data...")

    # Calculate per-index sentiment
    index_sentiments = get_index_sentiments(articles)
    nifty_sent = index_sentiments["nifty"]["sentiment"]
    banknifty_sent = index_sentiments["banknifty"]["sentiment"]
    nifty_score = index_sentiments["nifty"]["score"]
    banknifty_score = index_sentiments["banknifty"]["score"]
    logger.info(f"  Nifty: {nifty_sent.upper()} ({nifty_score:+.2f}) from {index_sentiments['nifty']['article_count']} articles")
    logger.info(f"  BankNifty: {banknifty_sent.upper()} ({banknifty_score:+.2f}) from {index_sentiments['banknifty']['article_count']} articles")

    # Score articles with per-index relevance
    NIFTY_KW = ["nifty", "sensex", "nse", "bse", "fii", "dii", "index", "benchmark", "mid-cap", "large-cap"]
    BANKNIFTY_KW = ["bank nifty", "banknifty", "banking", "bank", "hdfc bank", "icici bank", "sbi", "pnb", "axis", "kotak", "nbfc"]
    GENERAL_KW = ["rbi", "repo rate", "cpi", "inflation", "fed", "budget", "crash", "surge", "global"]

    for a in articles:
        title_lower = a.get("title", "").lower()
        body_lower = (a.get("body") or "").lower()[:500]
        text = f"{title_lower} {body_lower}"

        nifty_rel = sum(2 if kw in text else 0 for kw in NIFTY_KW)
        banknifty_rel = sum(2 if kw in text else 0 for kw in BANKNIFTY_KW)
        general = sum(1 if kw in text else 0 for kw in GENERAL_KW)
        if "nifty 50" in text or "sensex" in text:
            nifty_rel += 5
        if "bank nifty" in text or "banknifty" in text:
            banknifty_rel += 5

        sent_boost = 0.15 if a.get("sentiment_label") in ("bullish", "bearish") else 0
        base = a.get("sentiment_score", 0.5)

        a["_score_nifty"] = base + sent_boost + min(nifty_rel * 0.05, 1.0) + general * 0.05
        a["_score_banknifty"] = base + sent_boost + min(banknifty_rel * 0.05, 1.0) + general * 0.05

    top_nifty = sorted(articles, key=lambda a: a.get("_score_nifty", 0), reverse=True)[:5]
    top_banknifty = sorted(articles, key=lambda a: a.get("_score_banknifty", 0), reverse=True)[:5]
    logger.info(f"  Nifty top: {[a['title'][:30] for a in top_nifty]}")
    logger.info(f"  BankNifty top: {[a['title'][:30] for a in top_banknifty]}")

    # Build per-index items
    def build_items(article_list, sentiment_label):
        items_list = []
        for i, a in enumerate(article_list[:5]):
            items_list.append({
                "id": a.get("id", str(i)),
                "headline": a.get("title", "")[:120],
                "impact_text": f"Sentiment: {a.get('sentiment_label', 'neutral').upper()} with {a.get('sentiment_score', 0.5):.0%} confidence.",
                "sentiment_label": a.get("sentiment_label", "neutral"),
                "sentiment_score": a.get("sentiment_score", 0.5),
                "why": a.get("why", []),
                "sectors": a.get("sectors", {}),
                "stocks": a.get("stocks", []),
                "historical_context_nifty": "",
                "historical_context_banknifty": "",
                "source": a.get("source", ""),
                "url": a.get("url", ""),
                "order_index": i,
            })
            # Add nifty context based on index relevance
            title_lower = a.get("title", "").lower()
            nifty_rel = sum(2 if kw in title_lower else 0 for kw in NIFTY_KW)
            banknifty_rel = sum(2 if kw in title_lower else 0 for kw in BANKNIFTY_KW)
            items_list[i]["_nifty_rel"] = nifty_rel
            items_list[i]["_banknifty_rel"] = banknifty_rel
        return items_list

    nifty_items = build_items(top_nifty, nifty_sent)
    banknifty_items = build_items(top_banknifty, banknifty_sent)

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

            if nifty_items:
                nifty_items[0]["historical_context_nifty"] = hist_summary_nifty
            if banknifty_items:
                banknifty_items[0]["historical_context_banknifty"] = hist_summary_banknifty
        except Exception:
            pass

    # Build summary text with per-index breakdown
    summary_parts = [f"Market sentiment is mixed."]
    summary_parts.append(f"Nifty: {nifty_sent.upper()} (score: {nifty_score:+.2f}).")
    summary_parts.append(f"BankNifty: {banknifty_sent.upper()} (score: {banknifty_score:+.2f}).")

    if main_event:
        if hist_summary_nifty:
            summary_parts.append(f"Nifty: {hist_summary_nifty}")
        if hist_summary_banknifty:
            summary_parts.append(f"BankNifty: {hist_summary_banknifty}")

    fii_val = fii_data.get("fii_equity_cr", 0) or fii_data.get("fii_index_fut_cr", 0) or 0
    if fii_val != 0:
        fii_dir = "buying" if fii_val > 0 else "selling"
        summary_parts.append(f"FIIs {fii_dir} ₹{abs(fii_val):,.0f}cr.")

    summary_text = " ".join(summary_parts)

    # Build per-index summary texts
    summary_nifty = f"Nifty sentiment is {nifty_sent.upper()} (confidence {abs(nifty_score):.0%}). "
    if hist_summary_nifty:
        summary_nifty += hist_summary_nifty
    summary_banknifty = f"BankNifty sentiment is {banknifty_sent.upper()} (confidence {abs(banknifty_score):.0%}). "
    if hist_summary_banknifty:
        summary_banknifty += hist_summary_banknifty

    # Build per-index trade actions
    def trade_action(sentiment, index_name):
        if sentiment == "bullish":
            return f"Market sentiment for {index_name} is positive. Consider buying {index_name} calls or selling puts."
        elif sentiment == "bearish":
            return f"Market sentiment for {index_name} is negative. Consider buying {index_name} puts or selling calls."
        return f"{index_name} is neutral. Wait for clearer direction or trade range-bound strategies."

    trade_action_nifty = trade_action(nifty_sent, "Nifty")
    trade_action_banknifty = trade_action(banknifty_sent, "BankNifty")

    # Combine items into a unified item list (use nifty items as default, but store both separately)
    items = nifty_items

    brief_data = {
        "date": today,
        "overall_sentiment": "neutral",  # overall — will be overridden by per-index below
        "summary_text": summary_text,
        "items": items,
        "key_levels": key_levels,
        "historical_summary_nifty": hist_summary_nifty,
        "historical_summary_banknifty": hist_summary_banknifty,
        "accuracy": accuracy_stats,
        "created_at": datetime.now(timezone.utc).isoformat(),

        # PER-INDEX DATA — frontend toggle uses these
        "sentiment_nifty": nifty_sent,
        "sentiment_banknifty": banknifty_sent,
        "score_nifty": nifty_score,
        "score_banknifty": banknifty_score,
        "summary_nifty": summary_nifty,
        "summary_banknifty": summary_banknifty,
        "trade_action_nifty": trade_action_nifty,
        "trade_action_banknifty": trade_action_banknifty,
        "items_nifty": nifty_items,
        "items_banknifty": banknifty_items,
        "key_levels_nifty": key_levels,
        "key_levels_banknifty": key_levels,
        "index_sentiments": index_sentiments,
    }

    logger.info(f"  Nifty: {nifty_sent.upper()} / BankNifty: {banknifty_sent.upper()}")
    logger.info(f"  Summary: {summary_text[:80]}...")

    # ── Step 9: Save brief ──────────────────────────────────────
    logger.info("\nStep 9: Saving brief...")
    _save_json(BRIEF_PATH, brief_data)

    logger.info(f"\n✅ Done! Brief saved for {today}")


if __name__ == "__main__":
    run_pipeline()
