import { get } from './api'
import type { SentimentMeter } from '../types/brief'

export function fetchMeter(hours = 2): Promise<SentimentMeter> {
  return get<SentimentMeter>(`/meter?hours=${hours}`)
}
