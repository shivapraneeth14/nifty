import httpx
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging
import re

logger = logging.getLogger(__name__)

RSS_SOURCES = [
    {"name": "Moneycontrol", "url": "https://www.moneycontrol.com/rss/marketreports.xml"},
    {"name": "Economic Times", "url": "https://economictimes.indiatimes.com/markets/rss.cms"},
    {"name": "Mint", "url": "https://www.livemint.com/rss/money"},
    {"name": "NDTV Profit", "url": "https://www.ndtvprofit.com/rss/latest"},
    {"name": "CNBC TV18", "url": "https://www.cnbctv18.com/rss/market/"},
    {"name": "Zee Business", "url": "https://www.zeebiz.com/rss/market"},
]

MAX_PER_SOURCE = 8
TIMEOUT = httpx.Timeout(15.0, connect=10.0)


def _clean_xml(text: str) -> str:
    text = re.sub(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD\u10000-\u10FFF]', '', text)
    return text


def _is_market_relevant(title: str, body: str = "") -> bool:
    """Filter out non-market articles (personal finance, ITR, etc.)."""
    text = f"{title} {body}".lower()
    non_market = ["chatgpt", "side hustle", "credit card", "debt trap", "itr filing",
                  "epf", "mutual fund sip", "nps", "insurance", "tax saving",
                  "budget 202", "mango bond", "tree renting", "biker",
                  "how to save", "financial literacy", "retirement"]
    return not any(kw in text for kw in non_market)


def _parse_rss(source: dict) -> list[dict]:
    articles = []
    try:
        with httpx.Client(timeout=TIMEOUT, follow_redirects=True) as client:
            resp = client.get(source["url"])
            resp.raise_for_status()
            raw = resp.text

        raw = _clean_xml(raw)
        feed = feedparser.parse(raw)

        for entry in feed.entries[:MAX_PER_SOURCE]:
            raw_summary = entry.get("summary", "") or entry.get("description", "")
            body = BeautifulSoup(raw_summary, "lxml").get_text(separator=" ").strip()
            title = entry.get("title", "").strip()

            if not _is_market_relevant(title, body):
                continue

            published_at = datetime.now(timezone.utc).isoformat()
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
                except Exception:
                    pass

            articles.append({
                "title": title,
                "source": source["name"],
                "url": entry.get("link", ""),
                "body": body[:2000],
                "published_at": published_at,
                "sentiment_label": None,
                "sentiment_score": None,
            })
    except Exception as e:
        logger.error(f"RSS error for {source['name']}: {e}")
    return articles


def get_articles() -> list[dict]:
    all_articles = []
    for source in RSS_SOURCES:
        try:
            fetched = _parse_rss(source)
            logger.info(f"  {source['name']}: {len(fetched)} articles")
            all_articles.extend(fetched)
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")

    seen_urls = set()
    unique = []
    for a in all_articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            unique.append(a)

    unique = [a for a in unique if len(a.get("title", "")) > 10]
    logger.info(f"Total unique articles: {len(unique)}")
    return unique
