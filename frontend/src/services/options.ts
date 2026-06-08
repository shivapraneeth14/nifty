import { get } from './api'
import type { OptionChain } from '../types/brief'

export function fetchOptionChain(): Promise<OptionChain> {
  return get<OptionChain>('/options')
}
