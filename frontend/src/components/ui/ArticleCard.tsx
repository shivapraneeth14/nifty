import { useNavigate } from 'react-router-dom'
import SentimentBadge from './SentimentBadge'
import type { Article } from '../../types/article'

export default function ArticleCard({ article }: { article: Article }) {
  const navigate = useNavigate()
  return (
    <div onClick={() => navigate(`/article/${article.id}`)} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 hover:border-indigo-500/30 cursor-pointer transition-all duration-200">
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-sm font-medium leading-snug text-gray-900 dark:text-gray-100">{article.title}</h3>
        {article.sentiment_label && <SentimentBadge label={article.sentiment_label} score={article.sentiment_score} />}
      </div>
      <div className="flex items-center gap-2 mt-2 text-[10px] text-gray-400 dark:text-gray-500">
        <span className="font-medium">{article.source}</span>
        <span>·</span>
        <span>{new Date(article.published_at).toLocaleDateString()}</span>
      </div>
    </div>
  )
}
