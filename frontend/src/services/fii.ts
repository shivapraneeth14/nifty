import { get } from './api'
import type { Fiidata } from '../types/brief'

export function fetchFiidata(): Promise<Fiidata> {
  return get<Fiidata>('/fii')
}
