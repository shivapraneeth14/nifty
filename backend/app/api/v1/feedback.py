from fastapi import APIRouter
from pathlib import Path
import json
import logging

router = APIRouter(prefix="/feedback", tags=["feedback"])

logger = logging.getLogger(__name__)

FEEDBACK_PATH = Path(__file__).parent.parent.parent.parent / "data" / "feedback.json"


@router.post("")
def submit_feedback(fb: dict):
    try:
        feedback_data = []
        try:
            with open(FEEDBACK_PATH) as f:
                feedback_data = json.load(f)
        except Exception:
            pass

        if not isinstance(feedback_data, list):
            feedback_data = []

        fb["created_at"] = __import__("datetime").datetime.now().isoformat()
        feedback_data.append(fb)

        with open(FEEDBACK_PATH, "w") as f:
            json.dump(feedback_data, f, indent=2)

        return {"success": True}

    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        return {"error": str(e)}
