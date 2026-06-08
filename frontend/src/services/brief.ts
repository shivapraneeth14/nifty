import { get } from './api'
import type { Brief } from '../types/brief'

export function fetchTodayBrief(): Promise<Brief> {
  return get<Brief>('/brief/today')
}
