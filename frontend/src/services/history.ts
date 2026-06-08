import { get } from './api'
import type { HistoricalEvent } from '../types/history'

interface HistoryResponse { events: HistoricalEvent[] }

export function fetchHistory(event_type?: string): Promise<HistoryResponse> {
  const q = event_type ? `?event_type=${event_type}` : ''
  return get<HistoryResponse>(`/history${q}`)
}
