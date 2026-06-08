from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])

FCM_TOKENS_PATH = Path(__file__).parent.parent.parent.parent / "data" / "fcm_tokens.json"


class RegisterDevice(BaseModel):
    token: str
    platform: str = "web"
    enabled: bool = True


@router.post("/register")
def register_device(device: RegisterDevice):
    try:
        tokens = []
        try:
            with open(FCM_TOKENS_PATH) as f:
                tokens = json.load(f)
        except Exception:
            pass
        if not isinstance(tokens, list):
            tokens = []

        # Update or add
        existing = [t for t in tokens if t.get("token") != device.token]
        existing.append(device.model_dump())
        with open(FCM_TOKENS_PATH, "w") as f:
            json.dump(existing, f, indent=2)

        return {"success": True}
    except Exception as e:
        logger.error(f"Failed to register device: {e}")
        return {"error": str(e)}


@router.post("/send-test")
def send_test():
    """Placeholder for FCM push — requires Firebase project setup."""
    return {"message": "Push notifications require Firebase project setup. See README for instructions."}
