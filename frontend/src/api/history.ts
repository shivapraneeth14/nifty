import { get } from './client'
import type { HistoricalEvent } from '../types/history'

interface HistoryResponse {
  events: HistoricalEvent[]
}

export function fetchHistory(event_type?: string): Promise<HistoryResponse> {
  const query = event_type ? `?event_type=${event_type}` : ''
  return get<HistoryResponse>(`/history${query}`)
}
