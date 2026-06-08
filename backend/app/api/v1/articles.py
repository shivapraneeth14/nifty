from fastapi import APIRouter, Query
from app.database import supabase

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("")
def list_articles(
    date: str = Query(None),
    source: str = Query(None),
    limit: int = Query(20, le=50),
    offset: int = Query(0),
):
    try:
        query = supabase.table("articles").select("*").order("published_at", desc=True)

        if date:
            query = query.eq("published_at::date", date)
        if source:
            query = query.eq("source", source)

        result = query.range(offset, offset + limit - 1).execute()
        return {"articles": result.data or [], "offset": offset, "limit": limit}
    except Exception as e:
        return {"error": str(e)}
