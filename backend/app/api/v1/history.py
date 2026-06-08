from fastapi import APIRouter, Query
from app.database import supabase

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def get_history(event_type: str = Query(None), limit: int = Query(20, le=50)):
    try:
        query = supabase.table("historical_events").select("*").order("date", desc=True)
        if event_type:
            query = query.eq("event_type", event_type.upper())
        result = query.limit(limit).execute()
        return {"events": result.data or []}
    except Exception as e:
        return {"error": str(e)}
