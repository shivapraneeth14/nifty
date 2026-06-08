export interface Article {
  id: string
  title: string
  source: string
  url: string
  body: string | null
  published_at: string
  sentiment_label: 'bullish' | 'bearish' | 'neutral' | null
  sentiment_score: number | null
  created_at: string
}
