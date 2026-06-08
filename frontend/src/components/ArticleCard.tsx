import { Link } from 'react-router-dom'
import SentimentBadge from './SentimentBadge'
import type { Article } from '../types/article'

interface Props {
  article: Article
}

export default function ArticleCard({ article }: Props) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="block border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition"
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-medium text-sm leading-snug">{article.title}</h3>
        {article.sentiment_label && (
          <SentimentBadge label={article.sentiment_label} score={article.sentiment_score} />
        )}
      </div>
      <div className="flex items-center gap-2 mt-2 text-xs text-gray-400">
        <span>{article.source}</span>
        <span>·</span>
        <span>{new Date(article.published_at).toLocaleDateString()}</span>
      </div>
    </Link>
  )
}
