from fastapi import APIRouter
from datetime import date
from app.database import supabase

router = APIRouter(prefix="/brief", tags=["brief"])


@router.get("/today")
def get_today_brief():
    today = date.today().isoformat()
    try:
        brief = (
            supabase.table("briefs")
            .select("*")
            .eq("date", today)
            .limit(1)
            .execute()
        )
        if not brief.data:
            return {"date": today, "overall_sentiment": "neutral", "summary_text": "Brief not yet generated for today.", "items": []}

        brief_data = brief.data[0]
        items = (
            supabase.table("brief_items")
            .select("*")
            .eq("brief_id", brief_data["id"])
            .order("order_index")
            .execute()
        )

        enriched_items = []
        for item in (items.data or []):
            article_id = item.get("article_id")
            sentiment_label = None
            sentiment_score = None
            if article_id:
                article = supabase.table("articles").select("sentiment_label, sentiment_score").eq("id", article_id).limit(1).execute()
                if article.data:
                    sentiment_label = article.data[0].get("sentiment_label")
                    sentiment_score = article.data[0].get("sentiment_score")
            item["sentiment_label"] = sentiment_label
            item["sentiment_score"] = sentiment_score
            enriched_items.append(item)

        brief_data["items"] = enriched_items
        return brief_data
    except Exception as e:
        return {"error": str(e)}
