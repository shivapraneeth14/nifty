import SentimentBadge from './SentimentBadge'
import FeedbackButtons from './FeedbackButtons'
import type { BriefItem } from '../types/brief'

interface Props {
  item: BriefItem
  briefId: string
  index?: 'nifty' | 'banknifty'
}

export default function BriefCard({ item, briefId, index = 'nifty' }: Props) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 space-y-2">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-sm leading-snug">{item.headline}</h3>
        <SentimentBadge label={item.sentiment_label} score={item.sentiment_score} />
      </div>

      <p className="text-sm text-gray-600">{item.impact_text}</p>

      {item.historical_context && index === 'nifty' && (
        <p className="text-xs text-blue-700 bg-blue-50 px-2 py-1 rounded">
          📊 {item.historical_context}
        </p>
      )}

      <div className="flex items-center justify-between text-xs text-gray-400">
        <span>{item.source}</span>
        <FeedbackButtons briefId={briefId} articleId={item.article_id || undefined} />
      </div>
    </div>
  )
}
