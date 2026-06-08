import { get } from './api'
import type { GlobalMarketPulse } from '../types/brief'

export function fetchGlobalMarketPulse(): Promise<GlobalMarketPulse> {
  return get<GlobalMarketPulse>('/market/global')
}
