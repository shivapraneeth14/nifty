import yfinance as yf
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

GLOBAL_MARKET_PATH = Path(__file__).parent.parent.parent / "data" / "global_market.json"


def _get_change(ticker: str, period: str = "2d") -> dict:
    """Get latest price and change for a ticker."""
    try:
        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if data.empty:
            return {"price": None, "change_pct": None}
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2] if len(data) > 1 else last
        change_pct = round((last - prev) / prev * 100, 2) if prev != 0 else 0
        return {"price": round(float(last), 2), "change_pct": change_pct}
    except Exception as e:
        logger.warning(f"Failed to fetch {ticker}: {e}")
        return {"price": None, "change_pct": None}


def get_global_market_pulse() -> dict:
    """Fetch all global market data points."""
    result = {
        "sgx_nifty": _get_change("^SGXNIFTY"),
        "dow_futures": _get_change("YM=F"),
        "crude_oil": _get_change("CL=F"),
        "usd_inr": _get_change("INR=X"),
        "us_10y": _get_change("^TNX"),
        "vix": _get_change("^INDIAVIX"),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Add plain-English interpretation
    result["summary"] = _generate_summary(result)

    try:
        with open(GLOBAL_MARKET_PATH, "w") as f:
            json.dump(result, f, indent=2)
    except Exception:
        pass

    return result


def _generate_summary(data: dict) -> str:
    parts = []

    sgx = data.get("sgx_nifty", {})
    if sgx.get("change_pct") is not None:
        direction = "up" if sgx["change_pct"] > 0 else "down"
        parts.append(f"SGX Nifty {direction} {abs(sgx['change_pct']):.1f}%")

    crude = data.get("crude_oil", {})
    if crude.get("change_pct") is not None:
        direction = "up" if crude["change_pct"] > 0 else "down"
        parts.append(f"Crude {direction} {abs(crude['change_pct']):.1f}%")

    usd = data.get("usd_inr", {})
    if usd.get("price") is not None:
        parts.append(f"USD/INR {usd['price']:.2f}")

    dow = data.get("dow_futures", {})
    if dow.get("change_pct") is not None:
        direction = "up" if dow["change_pct"] > 0 else "down"
        parts.append(f"Dow futures {direction} {abs(dow['change_pct']):.1f}%")

    if not parts:
        return "Global market data unavailable"

    return " · ".join(parts)
