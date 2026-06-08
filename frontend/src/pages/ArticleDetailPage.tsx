import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchArticles } from '../api/articles'
import type { Article } from '../types/article'
import SentimentBadge from '../components/SentimentBadge'

export default function ArticleDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [article, setArticle] = useState<Article | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetchArticles({ limit: 50 })
      .then((res) => {
        const found = res.articles.find((a) => a.id === id)
        setArticle(found || null)
      })
      .catch(() => setArticle(null))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return <div className="py-20 text-center text-gray-400">Loading...</div>
  }

  if (!article) {
    return (
      <div className="py-20 text-center text-gray-400">
        <p>Article not found</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-bold leading-snug">{article.title}</h1>

      <div className="flex items-center gap-3">
        {article.sentiment_label && (
          <SentimentBadge label={article.sentiment_label} score={article.sentiment_score} />
        )}
        <span className="text-xs text-gray-400">{article.source}</span>
        <span className="text-xs text-gray-400">
          {new Date(article.published_at).toLocaleString()}
        </span>
      </div>

      {article.body && (
        <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
          {article.body}
        </p>
      )}

      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block text-sm text-blue-600 underline"
      >
        Read full article →
      </a>
    </div>
  )
}
