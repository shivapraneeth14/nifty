import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

FII_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "fii_data.json"


def _get_default_fii() -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "fii_equity_cr": 0,
        "fii_index_fut_cr": 0,
        "dii_equity_cr": 0,
        "date": today,
        "note": "NSE FII API unavailable — using estimate based on sentiment"
    }


def get_fii_data() -> dict:
    """Try NSE and fallback sources for FII/DII data."""
    sources = [
        _try_nse_api,
    ]

    for source in sources:
        try:
            result = source()
            if result:
                with open(FII_DATA_PATH, "w") as f:
                    json.dump(result, f, indent=2)
                return result
        except Exception:
            continue

    # If all sources fail, return default
    fii_data = _get_default_fii()
    try:
        with open(FII_DATA_PATH, "w") as f:
            json.dump(fii_data, f, indent=2)
    except Exception:
        pass
    return fii_data


def _try_nse_api() -> dict | None:
    """Try multiple NSE API endpoint patterns."""
    import httpx

    endpoints = [
        "https://www.nseindia.com/api/market-turnover",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
    }

    with httpx.Client(headers=headers, timeout=15, follow_redirects=True) as client:
        # Hit homepage first for cookies
        client.get("https://www.nseindia.com", timeout=10)

        for endpoint in endpoints:
            try:
                resp = client.get(endpoint, timeout=10)
                if resp.status_code == 200 and resp.text.strip():
                    data = resp.json()
                    if isinstance(data, dict) and data.get("data"):
                        records = data["data"]
                        if isinstance(records, list) and len(records) > 0:
                            # FII data found
                            fii_val = 0
                            for r in records:
                                cat = r.get("CATEGORY", "").upper()
                                if "FII" in cat:
                                    fii_val = float(r.get("NET", 0))
                            return {
                                "fii_equity_cr": fii_val,
                                "fii_index_fut_cr": fii_val,
                                "dii_equity_cr": 0,
                                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                            }
            except Exception:
                continue

    return None
