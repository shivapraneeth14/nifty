export interface BriefItem {
  id: string
  brief_id: string
  article_id: string | null
  headline: string
  impact_text: string
  historical_context: string
  order_index: number
  sentiment_label: 'bullish' | 'bearish' | 'neutral'
  source: string
  url: string
}

export interface Brief {
  id: string
  date: string
  overall_sentiment: 'bullish' | 'bearish' | 'neutral'
  summary_text: string
  created_at: string
  items: BriefItem[]
}
