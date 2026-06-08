import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from app.database import supabase

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)

HISTORICAL_EVENTS = [
    {"event_type": "RBI", "date": "2024-10-09", "headline": "RBI holds repo rate at 6.5%, shifts stance to neutral", "nifty_move": 218.0, "banknifty_move": 580.0, "sentiment_after": "bullish"},
    {"event_type": "RBI", "date": "2024-08-08", "headline": "RBI keeps repo rate unchanged at 6.5%", "nifty_move": 145.0, "banknifty_move": 320.0, "sentiment_after": "neutral"},
    {"event_type": "RBI", "date": "2024-06-07", "headline": "RBI holds repo rate at 6.5%, GDP forecast raised to 7.2%", "nifty_move": 382.0, "banknifty_move": 820.0, "sentiment_after": "bullish"},
    {"event_type": "RBI", "date": "2024-04-05", "headline": "RBI holds repo rate, maintains withdrawal of accommodation", "nifty_move": -78.0, "banknifty_move": -210.0, "sentiment_after": "neutral"},
    {"event_type": "RBI", "date": "2024-02-08", "headline": "RBI keeps repo rate at 6.5%, cautious on inflation", "nifty_move": 115.0, "banknifty_move": 280.0, "sentiment_after": "neutral"},
    {"event_type": "RBI", "date": "2023-12-08", "headline": "RBI holds repo rate at 6.5% for fifth straight time", "nifty_move": 333.0, "banknifty_move": 760.0, "sentiment_after": "bullish"},
    {"event_type": "RBI", "date": "2023-04-06", "headline": "RBI surprises with pause after 250bps rate hike cycle", "nifty_move": 374.0, "banknifty_move": 890.0, "sentiment_after": "bullish"},
    {"event_type": "RBI", "date": "2023-02-08", "headline": "RBI hikes repo rate by 25bps to 6.5%", "nifty_move": -238.0, "banknifty_move": -560.0, "sentiment_after": "bearish"},
    {"event_type": "FED", "date": "2024-09-18", "headline": "Fed cuts rates by 50bps in surprise move", "nifty_move": 428.0, "banknifty_move": 980.0, "sentiment_after": "bullish"},
    {"event_type": "FED", "date": "2024-07-31", "headline": "Fed holds rates, signals September cut likely", "nifty_move": 315.0, "banknifty_move": 720.0, "sentiment_after": "bullish"},
    {"event_type": "FED", "date": "2024-05-01", "headline": "Fed holds rates at 5.25%-5.5%, no near-term cuts", "nifty_move": -156.0, "banknifty_move": -380.0, "sentiment_after": "bearish"},
    {"event_type": "FED", "date": "2024-03-20", "headline": "Fed holds rates, projects 3 cuts in 2024", "nifty_move": 192.0, "banknifty_move": 430.0, "sentiment_after": "bullish"},
    {"event_type": "FED", "date": "2023-07-26", "headline": "Fed hikes 25bps, signals near end of tightening cycle", "nifty_move": 67.0, "banknifty_move": 150.0, "sentiment_after": "neutral"},
    {"event_type": "CPI", "date": "2024-11-12", "headline": "India CPI surges to 6.21% in Oct, above RBI tolerance", "nifty_move": -264.0, "banknifty_move": -620.0, "sentiment_after": "bearish"},
    {"event_type": "CPI", "date": "2024-10-14", "headline": "India CPI eases to 5.49% in September 2024", "nifty_move": 180.0, "banknifty_move": 410.0, "sentiment_after": "bullish"},
    {"event_type": "CPI", "date": "2024-06-12", "headline": "India CPI eases to 4.75% in May", "nifty_move": 208.0, "banknifty_move": 490.0, "sentiment_after": "bullish"},
    {"event_type": "CPI", "date": "2024-04-12", "headline": "India CPI at 4.85%, above estimates", "nifty_move": -112.0, "banknifty_move": -260.0, "sentiment_after": "bearish"},
    {"event_type": "BUDGET", "date": "2024-07-23", "headline": "Union Budget 2024: Capex maintained, LTCG hiked to 12.5%", "nifty_move": -577.0, "banknifty_move": -1380.0, "sentiment_after": "bearish"},
    {"event_type": "BUDGET", "date": "2024-02-01", "headline": "Interim Budget 2024: No major changes, fiscal consolidation", "nifty_move": 355.0, "banknifty_move": 820.0, "sentiment_after": "bullish"},
    {"event_type": "BUDGET", "date": "2023-02-01", "headline": "Budget 2023: Capex up 33%, income tax relief announced", "nifty_move": 817.0, "banknifty_move": 1780.0, "sentiment_after": "bullish"},
    {"event_type": "GDP", "date": "2024-11-29", "headline": "India Q2 GDP slows to 5.4%, below 6.5% estimate", "nifty_move": -346.0, "banknifty_move": -820.0, "sentiment_after": "bearish"},
    {"event_type": "GDP", "date": "2024-05-31", "headline": "India FY24 GDP at 8.2%, beats estimate of 7.6%", "nifty_move": 422.0, "banknifty_move": 980.0, "sentiment_after": "bullish"},
    {"event_type": "EARNINGS", "date": "2024-07-15", "headline": "TCS Q1 results beat estimates, stock gains 3%", "nifty_move": 145.0, "banknifty_move": 310.0, "sentiment_after": "bullish"},
    {"event_type": "GLOBAL", "date": "2024-08-05", "headline": "Global sell-off: Japan Nikkei crashes 12%, VIX spikes", "nifty_move": -483.0, "banknifty_move": -1120.0, "sentiment_after": "bearish"},
]


def seed():
    logger.info(f"Seeding {len(HISTORICAL_EVENTS)} historical events...")
    try:
        result = supabase.table("historical_events").upsert(
            HISTORICAL_EVENTS, on_conflict="event_type,date"
        ).execute()
        logger.info(f"✅ Seeded {len(result.data or [])} events")
    except Exception as e:
        logger.error(f"Error seeding: {e}")
        raise


if __name__ == "__main__":
    seed()
