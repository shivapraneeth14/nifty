export interface HistoricalEvent {
  id: string
  event_type: string
  date: string
  headline: string
  nifty_move: number | null
  banknifty_move: number | null
  sentiment_after: string | null
}
