import { get } from './api'
import type { Debrief } from '../types/brief'

export function fetchDebrief(): Promise<Debrief> {
  return get<Debrief>('/debrief')
}
