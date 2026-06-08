from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/accuracy", tags=["accuracy"])

ACCURACY_PATH = Path(__file__).parent.parent.parent.parent / "data" / "accuracy.json"


@router.get("")
def get_accuracy():
    try:
        with open(ACCURACY_PATH) as f:
            records = json.load(f)
    except Exception:
        return {"last_10": 0, "last_30": 0, "total": 0, "count": 0, "recent_days": []}

    if not isinstance(records, list):
        return {"last_10": 0, "last_30": 0, "total": 0, "count": 0, "recent_days": []}

    sorted_records = sorted(records, key=lambda r: r.get("date", ""), reverse=True)

    def calc(subset):
        correct = sum(1 for r in subset if r.get("correct") is True)
        total = sum(1 for r in subset if r.get("correct") is not None)
        return correct, total

    c10, t10 = calc(sorted_records[:10])
    c30, t30 = calc(sorted_records[:30])
    c_all, t_all = calc(sorted_records)

    return {
        "last_10": round(c10 / t10 * 100) if t10 > 0 else 0,
        "last_30": round(c30 / t30 * 100) if t30 > 0 else 0,
        "total": round(c_all / t_all * 100) if t_all > 0 else 0,
        "count": t_all,
        "recent_days": [r for r in sorted_records[:14] if r.get("correct") is not None],
    }
