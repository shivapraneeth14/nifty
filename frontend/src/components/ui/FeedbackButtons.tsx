import { useState } from 'react'
import { submitFeedback } from '../../services/feedback'
import { ThumbsUp, ThumbsDown } from 'lucide-react'

export default function FeedbackButtons({ briefId, articleId }: { briefId: string; articleId?: string }) {
  const [sent, setSent] = useState(false)

  const handle = async (helpful: boolean) => {
    await submitFeedback({ brief_id: briefId, article_id: articleId, helpful })
    setSent(true)
  }

  if (sent) return <span className="text-[10px] text-green-500 font-medium">✓ Thanks</span>

  return (
    <div className="flex items-center gap-1">
      <button onClick={() => handle(true)} className="p-1 rounded hover:bg-green-500/10 text-gray-400 hover:text-green-500 transition-colors">
        <ThumbsUp size={12} />
      </button>
      <button onClick={() => handle(false)} className="p-1 rounded hover:bg-red-500/10 text-gray-400 hover:text-red-500 transition-colors">
        <ThumbsDown size={12} />
      </button>
    </div>
  )
}
