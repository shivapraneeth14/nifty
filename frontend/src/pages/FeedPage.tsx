import { useEffect, useState, useCallback, useRef } from 'react'
import { fetchArticles } from '../api/articles'
import type { Article } from '../types/article'
import ArticleCard from '../components/ArticleCard'

export default function FeedPage() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [hasMore, setHasMore] = useState(true)
  const offset = useRef(0)
  const loadingRef = useRef(false)

  const load = useCallback(async () => {
    if (loadingRef.current || !hasMore) return
    loadingRef.current = true
    setLoading(true)
    try {
      const res = await fetchArticles({ limit: 10, offset: offset.current })
      if (res.articles.length < 10) setHasMore(false)
      setArticles((prev) => [...prev, ...res.articles])
      offset.current += res.articles.length
    } catch {
      // ignore
    } finally {
      setLoading(false)
      loadingRef.current = false
    }
  }, [hasMore])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    const onScroll = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 400) {
        load()
      }
    }
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [load])

  return (
    <div className="space-y-3">
      <h1 className="text-lg font-bold">Live News Feed</h1>
      {articles.map((a) => (
        <ArticleCard key={a.id} article={a} />
      ))}
      {loading && <p className="text-center text-gray-400 py-4">Loading more...</p>}
      {!hasMore && <p className="text-center text-gray-300 text-sm py-4">All caught up</p>}
    </div>
  )
}
