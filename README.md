# Nifty Brief

AI-powered pre-market trading brief for Indian Nifty 50 & Bank Nifty options traders.

## What it does

- Scrapes financial news (Moneycontrol, Mint, ET) every weekday at 8AM IST
- Analyzes sentiment with FinBERT (bullish/bearish/neutral per article)
- Matches news to historical events (RBI, Fed, CPI, Budget, GDP)
- Generates a 5-item pre-market brief with:
  - **Sentiment score** per article + overall market direction
  - **"Why does this matter?"** nursery-level explanations
  - **Sector impact** + **key stocks** to watch
  - **Historical context** — "Last 8 RBI events: up avg 198 pts"
  - **Nifty 50 / Bank Nifty toggle**
  - **Key levels** — Support, Resistance, PCR, FII data
  - **Accuracy tracker** — "8/10 correct last 10 days"

## Architecture

```
                     ┌──────────────────┐
                     │  GitHub Actions   │
                     │  8AM IST cron     │
                     └────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         [Scraper]      [FinBERT]      [Knowledge Base]
          RSS feeds      sentiment       cause-effect
          15 articles     per article     explanations
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  Brief Generator │
                     │  → scores top 5  │
                     │  → adds FII data │
                     │  → adds levels   │
                     │  → saves to JSON │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   FastAPI API     │
                     │  localhost:8080   │
                     │  /brief/today     │
                     │  /articles        │
                     │  /history         │
                     │  /feedback        │
                     │  /accuracy        │
                     │  /health          │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  React Frontend   │
                     │  localhost:3000   │
                     │  Dark/Light mode  │
                     │  Bottom tab nav   │
                     │  5 screens        │
                     └──────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS + Framer Motion |
| Backend | FastAPI + Python 3.11+ |
| AI | FinBERT (HuggingFace Transformers) |
| Data | JSON files (no database needed) |
| Automation | GitHub Actions (8AM IST daily) |
| UI Components | Lucide Icons, Inter + JetBrains Mono fonts |

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m scripts.daily_pipeline  # Scrape + analyze + generate brief
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev  # → localhost:3000
```

### Or use Make

```bash
cd backend
make run       # Start API server
make pipeline  # Run daily brief generation
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/brief/today` | Today's pre-market brief |
| GET | `/api/v1/articles` | All scraped articles (paginated) |
| GET | `/api/v1/history` | Historical events (filter by type) |
| GET | `/api/v1/accuracy` | Accuracy stats (last 10/30/all) |
| POST | `/api/v1/feedback` | Submit thumbs up/down |
| GET | `/health` | Health check |

## Data

All data stored as JSON files in `backend/data/`:
- `brief.json` — Latest generated brief
- `articles.json` — All scraped articles
- `historical_events.json` — 28 curated events (RBI, Fed, CPI, etc.)
- `knowledge_base.json` — Cause-effect explanations (7 event types × 3 modifiers each)
- `fii_data.json` — FII/DII net buy/sell data
- `accuracy.json` — Prediction accuracy records
- `feedback.json` — User feedback

## Screens

1. **Pre-market Brief** — 5 cards with sentiment, explanations, sectors, stocks, historical context
2. **Live Feed** — Infinite scroll of all articles with sentiment badges
3. **Historical Impact** — Filterable table of past events + Nifty/BankNifty moves
4. **Accuracy Tracker** — Progress ring + day-by-day breakdown
5. **Settings** — Dark mode toggle, language options, notification settings

Why this exists: 90% of retail F&O traders lose money. One reason is information overload — too much news, no context. Nifty Brief gives you the 5 things that matter, explained simply, before market opens.
