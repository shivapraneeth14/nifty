from fastapi import APIRouter
from datetime import date
from app.database import supabase

router = APIRouter(prefix="/brief", tags=["brief"])


def _summarize_moves(moves: list, label: str) -> str:
    if not moves:
        return ""
    avg = sum(moves) / len(moves)
    up = sum(1 for m in moves if m > 0)
    down = sum(1 for m in moves if m < 0)
    direction = "up" if avg > 0 else "down"
    return (
        f"Last {len(moves)} {label} events: "
        f"{direction} avg {abs(avg):.0f} pts "
        f"({up} times up, {down} times down)"
    )


def _build_index_summaries() -> dict:
    try:
        event_types = supabase.table("historical_events").select("event_type").order("date", desc=True).limit(1).execute()
        if not event_types.data:
            return {"nifty": "", "banknifty": ""}
        top_type = event_types.data[0]["event_type"]
        events = (
            supabase.table("historical_events")
            .select("nifty_move, banknifty_move")
            .eq("event_type", top_type)
            .order("date", desc=True)
            .limit(8)
            .execute()
        )
        if not events.data:
            return {"nifty": "", "banknifty": ""}
        nifty = [e["nifty_move"] for e in events.data if e.get("nifty_move") is not None]
        banknifty = [e["banknifty_move"] for e in events.data if e.get("banknifty_move") is not None]
        return {
            "nifty": _summarize_moves(nifty, top_type),
            "banknifty": _summarize_moves(banknifty, top_type),
        }
    except Exception:
        return {"nifty": "", "banknifty": ""}


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

        summaries = _build_index_summaries()
        brief_data["historical_summary_nifty"] = summaries["nifty"]
        brief_data["historical_summary_banknifty"] = summaries["banknifty"]

        return brief_data
    except Exception as e:
        return {"error": str(e)}
