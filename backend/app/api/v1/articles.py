from fastapi import APIRouter, Query
from pathlib import Path
import json

router = APIRouter(prefix="/articles", tags=["articles"])

ARTICLES_PATH = Path(__file__).parent.parent.parent.parent / "data" / "articles.json"


@router.get("")
def list_articles(
    date: str = Query(None),
    source: str = Query(None),
    limit: int = Query(20, le=50),
    offset: int = Query(0),
):
    try:
        with open(ARTICLES_PATH) as f:
            all_articles = json.load(f)
    except Exception:
        return {"articles": [], "offset": offset, "limit": limit}

    if not isinstance(all_articles, list):
        return {"articles": [], "offset": offset, "limit": limit}

    filtered = all_articles
    if source:
        filtered = [a for a in filtered if a.get("source") == source]

    # Sort by published_at descending
    filtered.sort(key=lambda a: a.get("published_at", ""), reverse=True)

    paginated = filtered[offset: offset + limit]

    return {"articles": paginated, "offset": offset, "limit": limit}
