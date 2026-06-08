import { useState } from 'react'
import { submitFeedback } from '../api/feedback'

interface Props {
  briefId: string
  articleId?: string
}

export default function FeedbackButtons({ briefId, articleId }: Props) {
  const [sent, setSent] = useState(false)

  const handle = async (helpful: boolean) => {
    await submitFeedback({ brief_id: briefId, article_id: articleId, helpful })
    setSent(true)
  }

  if (sent) {
    return <span className="text-xs text-gray-400">Thanks</span>
  }

  return (
    <div className="flex gap-2 mt-2">
      <button
        onClick={() => handle(true)}
        className="text-xs px-2 py-1 rounded border border-gray-300 hover:bg-green-50"
      >
        👍 Helpful
      </button>
      <button
        onClick={() => handle(false)}
        className="text-xs px-2 py-1 rounded border border-gray-300 hover:bg-red-50"
      >
        👎 Not helpful
      </button>
    </div>
  )
}
