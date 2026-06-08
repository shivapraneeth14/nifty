export interface BriefItem {
  id: string
  brief_id: string
  article_id: string | null
  headline: string
  impact_text: string
  historical_context: string
  historical_context_nifty?: string
  historical_context_banknifty?: string
  why?: string[]
  sectors?: Record<string, string>
  stocks?: string[]
  order_index: number
  sentiment_label: 'bullish' | 'bearish' | 'neutral'
  sentiment_score: number | null
  source: string
  url: string
}

export interface KeyLevels {
  support: number | null
  resistance: number | null
}

export interface Brief {
  id: string
  date: string
  overall_sentiment: 'bullish' | 'bearish' | 'neutral'
  summary_text: string
  created_at: string
  items: BriefItem[]
  historical_summary_nifty: string
  historical_summary_banknifty: string
  key_levels?: KeyLevels
  key_levels_nifty?: KeyLevels
  key_levels_banknifty?: KeyLevels
  accuracy?: {
    nifty: { last_10: number; count: number; recent_days?: { date: string; predicted: string; actual_move: number | null; correct: boolean | null }[] }
    banknifty: { last_10: number; count: number; recent_days?: { date: string; predicted: string; actual_move: number | null; correct: boolean | null }[] }
  }

  // Per-index data
  sentiment_nifty: 'bullish' | 'bearish' | 'neutral'
  sentiment_banknifty: 'bullish' | 'bearish' | 'neutral'
  score_nifty?: number
  score_banknifty?: number
  summary_nifty?: string
  summary_banknifty?: string
  trade_action_nifty?: string
  trade_action_banknifty?: string
  items_nifty?: BriefItem[]
  items_banknifty?: BriefItem[]
}

export interface GlobalMarketPulse {
  sgx_nifty: { price: number | null; change_pct: number | null }
  dow_futures: { price: number | null; change_pct: number | null }
  crude_oil: { price: number | null; change_pct: number | null }
  usd_inr: { price: number | null; change_pct: number | null }
  vix: { price: number | null; change_pct: number | null }
  summary: string
  updated_at: string
}

export interface SentimentMeter {
  nifty: number
  banknifty: number
  overall: 'bullish' | 'bearish' | 'neutral'
  article_count: number
  updated_at: string
}

export interface OptionChain {
  pcr_volume: number | null
  pcr_oi: number | null
  max_pain: number | null
  expiry: string | null
  total_call_oi: number
  total_put_oi: number
  interpretation: string
}

export interface Fiidata {
  fii_equity_cr: number
  fii_index_fut_cr: number
  dii_equity_cr: number
  date: string
  direction: string
  interpretation: string
}

export interface Debrief {
  date: string
  predicted_nifty?: string
  nifty_move?: number | null
  nifty_correct?: boolean | null
  predicted_banknifty?: string
  banknifty_move?: number | null
  banknifty_correct?: boolean | null
  debrief_text: string
  created_at: string
}
