-- Run this in Supabase Dashboard -> SQL Editor

CREATE TABLE IF NOT EXISTS articles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT NOT NULL,
    source          TEXT NOT NULL,
    url             TEXT UNIQUE NOT NULL,
    body            TEXT,
    published_at    TIMESTAMPTZ DEFAULT NOW(),
    sentiment_label TEXT CHECK (sentiment_label IN ('bullish','bearish','neutral')),
    sentiment_score FLOAT CHECK (sentiment_score BETWEEN 0 AND 1),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS briefs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date                DATE UNIQUE NOT NULL,
    overall_sentiment   TEXT CHECK (overall_sentiment IN ('bullish','bearish','neutral')),
    summary_text        TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brief_items (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brief_id            UUID NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    article_id          UUID REFERENCES articles(id) ON DELETE SET NULL,
    headline            TEXT NOT NULL,
    impact_text         TEXT,
    historical_context  TEXT DEFAULT '',
    order_index         INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS historical_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type      TEXT NOT NULL,
    date            DATE NOT NULL,
    headline        TEXT NOT NULL,
    nifty_move      FLOAT,
    banknifty_move  FLOAT,
    sentiment_after TEXT CHECK (sentiment_after IN ('bullish','bearish','neutral')),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_type, date)
);

CREATE TABLE IF NOT EXISTS feedback (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID,
    brief_id    UUID REFERENCES briefs(id) ON DELETE CASCADE,
    article_id  UUID REFERENCES articles(id) ON DELETE SET NULL,
    helpful     BOOLEAN NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_sentiment ON articles(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_briefs_date ON briefs(date DESC);
CREATE INDEX IF NOT EXISTS idx_brief_items_brief ON brief_items(brief_id, order_index);
CREATE INDEX IF NOT EXISTS idx_hist_event_type ON historical_events(event_type, date DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_brief ON feedback(brief_id);

ALTER PUBLICATION supabase_realtime ADD TABLE articles;
