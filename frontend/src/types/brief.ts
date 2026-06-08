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
