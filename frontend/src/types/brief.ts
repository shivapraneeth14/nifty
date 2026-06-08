export interface BriefItem {
  id: string
  brief_id: string
  article_id: string | null
  headline: string
  impact_text: string
  historical_context: string
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
  pcr: number | null
  fii_cr: number | null
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
  predicted: string
  actual_move: number | null
  correct: boolean | null
  debrief_text: string
  created_at: string
}
