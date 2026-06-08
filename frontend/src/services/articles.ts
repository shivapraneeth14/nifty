import { get } from './api'
import type { Article } from '../types/article'

interface ArticlesResponse {
  articles: Article[]
  offset: number
  limit: number
}

export function fetchArticles(params: { date?: string; source?: string; limit?: number; offset?: number }): Promise<ArticlesResponse> {
  const q = new URLSearchParams()
  if (params.date) q.set('date', params.date)
  if (params.source) q.set('source', params.source)
  if (params.limit) q.set('limit', String(params.limit))
  if (params.offset) q.set('offset', String(params.offset))
  return get<ArticlesResponse>(`/articles?${q}`)
}

export function fetchArticleById(id: string): Promise<Article | null> {
  return fetchArticles({ limit: 50 }).then((res) => res.articles.find((a) => a.id === id) || null)
}
