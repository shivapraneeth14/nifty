import { useState, useEffect } from 'react'
import type { Article } from '../types/article'
import { fetchArticles } from '../services/articles'

export function useArticles() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const offsetRef = { current: 0 }

  const load = async () => {
    if (!hasMore) return
    setLoading(true)
    try {
      const res = await fetchArticles({ limit: 10, offset: offsetRef.current })
      if (res.articles.length < 10) setHasMore(false)
      setArticles((prev) => [...prev, ...res.articles])
      offsetRef.current += res.articles.length
    } catch {
      // silent
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return { articles, loading, hasMore, loadMore: load }
}
