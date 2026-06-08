import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from datetime import date, datetime, timezone
from app.database import supabase
from app.services.scraper import get_articles
from app.services.sentiment import analyze_batch
from app.services.historical import get_relevant_history
from app.services.brief_generator import generate_brief

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("=" * 50)
    logger.info("  Nifty Brief — Daily Pipeline")
    logger.info(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    logger.info("=" * 50)

    today = date.today().isoformat()

    existing = supabase.table("briefs").select("id").eq("date", today).limit(1).execute()
    if existing.data:
        logger.info("Brief already exists for today — skipping")
        return

    logger.info("\nStep 1: Scraping articles...")
    articles = get_articles()
    if not articles:
        logger.error("No articles fetched")
        sys.exit(1)

    logger.info(f"\nStep 2: Analyzing {len(articles)} articles...")
    articles = analyze_batch(articles)

    logger.info("\nStep 3: Saving articles...")
    article_map = {}
    for a in articles:
        try:
            result = supabase.table("articles").upsert(a, on_conflict="url").execute()
            if result.data:
                article_map[a["url"]] = result.data[0].get("id")
        except Exception as e:
            logger.error(f"Error saving article: {e}")

    logger.info("\nStep 4: Fetching historical context...")
    historical = get_relevant_history(articles)
    logger.info(f"  Found {len(historical)} relevant events")

    logger.info("\nStep 5: Generating brief...")
    brief_data = generate_brief(articles, historical)
    logger.info(f"  Sentiment: {brief_data['overall_sentiment'].upper()}")
    logger.info(f"  Summary: {brief_data['summary_text'][:80]}")

    logger.info("\nStep 6: Saving brief...")
    brief_row = {
        "date": brief_data["date"],
        "overall_sentiment": brief_data["overall_sentiment"],
        "summary_text": brief_data["summary_text"],
        "created_at": brief_data["created_at"],
    }
    result = supabase.table("briefs").insert(brief_row).execute()
    brief_id = result.data[0]["id"]

    items = []
    for item in brief_data.get("items", []):
        items.append({
            "brief_id": brief_id,
            "article_id": article_map.get(item.get("url", "")),
            "headline": item["headline"],
            "impact_text": item.get("impact_text", ""),
            "historical_context": item.get("historical_context", ""),
            "order_index": item["order_index"],
        })
    if items:
        supabase.table("brief_items").insert(items).execute()

    logger.info(f"\n✅ Done! Brief ID: {brief_id}")


if __name__ == "__main__":
    run_pipeline()
