import { get } from './client'
import type { Brief } from '../types/brief'

export function fetchTodayBrief(): Promise<Brief> {
  return get<Brief>('/brief/today')
}
