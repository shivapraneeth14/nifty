import { get } from './client'
import type { Article } from '../types/article'

interface ArticlesResponse {
  articles: Article[]
  offset: number
  limit: number
}

export function fetchArticles(params: {
  date?: string
  source?: string
  limit?: number
  offset?: number
}): Promise<ArticlesResponse> {
  const query = new URLSearchParams()
  if (params.date) query.set('date', params.date)
  if (params.source) query.set('source', params.source)
  if (params.limit) query.set('limit', String(params.limit))
  if (params.offset) query.set('offset', String(params.offset))
  return get<ArticlesResponse>(`/articles?${query}`)
}
