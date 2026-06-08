from fastapi import APIRouter
from pydantic import BaseModel
from app.database import supabase

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackCreate(BaseModel):
    brief_id: str
    article_id: str | None = None
    helpful: bool
    user_id: str | None = None


@router.post("")
def submit_feedback(fb: FeedbackCreate):
    try:
        result = (
            supabase.table("feedback")
            .insert(fb.model_dump(exclude_none=True))
            .execute()
        )
        return {"success": True, "feedback_id": result.data[0]["id"]}
    except Exception as e:
        return {"error": str(e)}
