import yfinance as yf
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

OPTION_CHAIN_PATH = Path(__file__).parent.parent.parent / "data" / "option_chain.json"


def _get_options_data(ticker: str = "^NSEI") -> dict:
    """Fetch options chain and compute PCR, max pain, OI buildup."""
    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options
        if not expirations:
            return {}

        # Use nearest expiry
        nearest = expirations[0]
        opt = stock.option_chain(nearest)
        calls, puts = opt.calls, opt.puts

        if calls.empty or puts.empty:
            return {}

        # PCR (Put-Call Ratio) by volume
        total_call_vol = calls["volume"].sum() if "volume" in calls else 0
        total_put_vol = puts["volume"].sum() if "volume" in puts else 0
        pcr = round(total_put_vol / total_call_vol, 2) if total_call_vol > 0 else 1.0

        # PCR by OI (Open Interest)
        total_call_oi = calls["openInterest"].sum() if "openInterest" in calls else 0
        total_put_oi = puts["openInterest"].sum() if "openInterest" in puts else 0
        pcr_oi = round(total_put_oi / total_call_oi, 2) if total_call_oi > 0 else 1.0

        # Max Pain — the strike where max loss occurs for option buyers
        # Calculated as the strike with highest total premium (call premium + put premium)
        strikes = []
        for _, row in calls.iterrows():
            strike = row.get("strike", 0)
            call_premium = row.get("openInterest", 0) * row.get("lastPrice", 0)
            put_premium = 0
            put_row = puts[puts["strike"] == strike]
            if not put_row.empty:
                put_premium = put_row.iloc[0].get("openInterest", 0) * put_row.iloc[0].get("lastPrice", 0)
            strikes.append({"strike": strike, "total_premium": call_premium + put_premium})

        max_pain = max(strikes, key=lambda s: s["total_premium"])["strike"] if strikes else None

        # OI buildup — top 3 strikes with highest OI change
        calls_sorted = calls.nlargest(3, "openInterest")[["strike", "openInterest", "lastPrice"]] if "openInterest" in calls else []
        puts_sorted = puts.nlargest(3, "openInterest")[["strike", "openInterest", "lastPrice"]] if "openInterest" in puts else []

        return {
            "pcr_volume": pcr,
            "pcr_oi": pcr_oi,
            "max_pain": round(float(max_pain), 0) if max_pain else None,
            "expiry": nearest,
            "total_call_oi": int(total_call_oi),
            "total_put_oi": int(total_put_oi),
            "top_call_oi": calls_sorted.to_dict("records") if not calls_sorted.empty else [],
            "top_put_oi": puts_sorted.to_dict("records") if not puts_sorted.empty else [],
        }

    except Exception as e:
        logger.warning(f"Failed to fetch options data: {e}")
        return {}


def _generate_interpretation(data: dict) -> str:
    """Plain-English interpretation of option chain data."""
    parts = []
    pcr = data.get("pcr_volume")

    if pcr is not None:
        if pcr > 1.2:
            parts.append(f"PCR at {pcr} — ⚡ Above 1.2 means more PUTS being bought than CALLS. Market sentiment is BEARISH. Options traders expect downside.")
        elif pcr < 0.8:
            parts.append(f"PCR at {pcr} — 📈 Below 0.8 means more CALLS being bought than PUTS. Market sentiment is BULLISH. Options traders expect upside.")
        else:
            parts.append(f"PCR at {pcr} — ⚪ Between 0.8 and 1.2 means options market is balanced. No strong directional bias.")

    max_pain = data.get("max_pain")
    spot = data.get("spot_price")
    if max_pain and spot:
        diff = spot - max_pain
        if abs(diff) < 100:
            parts.append(f"Max Pain at {max_pain:.0f} — Market is near max pain level. Options sellers are in control. Expect price to stay near this level.")
        elif diff > 0:
            parts.append(f"Max Pain at {max_pain:.0f} (spot above). Market is above max pain — bullish bias for expiry.")

    if not parts:
        return "Option chain data unavailable. Check back during market hours."

    return " ".join(parts)


def get_option_chain() -> dict:
    """Get option chain snapshot with interpretation."""
    data = _get_options_data("^NSEI")
    if not data:
        try:
            # Fallback: try fetching with different ticker
            data = _get_options_data("NIFTY.NS")
        except Exception:
            data = {}

    if not data:
        return {
            "pcr_volume": None,
            "pcr_oi": None,
            "max_pain": None,
            "expiry": None,
            "interpretation": "Option chain data not available during non-market hours. Check back after 9:15 AM.",
        }

    data["interpretation"] = _generate_interpretation(data)

    try:
        with open(OPTION_CHAIN_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

    return data
