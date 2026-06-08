import { useEffect, useRef, useCallback } from 'react'
import { motion } from 'framer-motion'
import { useArticles } from '../hooks/useArticles'
import SentimentBadge from '../components/ui/SentimentBadge'
import { CardSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/ErrorState'
import { formatTime } from '../utils/formatters'

export default function FeedScreen() {
  const { articles, loading, hasMore, loadMore } = useArticles()
  const loaderRef = useRef<HTMLDivElement>(null)

  const handleScroll = useCallback(() => {
    if (!loaderRef.current) return
    const r = loaderRef.current.getBoundingClientRect()
    if (r.top < window.innerHeight + 400 && hasMore && !loading) loadMore()
  }, [hasMore, loading, loadMore])

  useEffect(() => { window.addEventListener('scroll', handleScroll); return () => window.removeEventListener('scroll', handleScroll) }, [handleScroll])

  if (!articles.length && loading) return <div className="space-y-3 pb-24"><h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Live Feed</h1>{[1,2,3].map(i => <CardSkeleton key={i} />)}</div>

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3 pb-24">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Live Feed</h1>
        <span className="flex items-center gap-1.5 text-[10px] font-medium text-green-500 bg-green-500/10 px-2 py-0.5 rounded-full">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />LIVE
        </span>
      </div>
      {articles.length === 0 && !loading ? (
        <EmptyState icon="📰" message="No articles yet" submessage="Articles appear after the morning pipeline runs" />
      ) : (
        <>
          {articles.map((a, i) => (
            <motion.div key={a.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}
              className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 hover:border-indigo-500/30 transition-colors"
            >
              <div className="flex items-start justify-between gap-3">
                <h3 className="text-sm font-medium leading-snug text-gray-900 dark:text-gray-100">{a.title}</h3>
                {a.sentiment_label && <SentimentBadge label={a.sentiment_label} score={a.sentiment_score} />}
              </div>
              <div className="flex items-center gap-2 mt-2 text-[10px] text-gray-400 dark:text-gray-500">
                <span className="font-medium">{a.source}</span><span>·</span><span>{formatTime(a.published_at)}</span>
              </div>
            </motion.div>
          ))}
          <div ref={loaderRef} className="py-4 text-center text-xs text-gray-400 dark:text-gray-500">
            {loading ? 'Loading more...' : hasMore ? 'Scroll for more' : 'All caught up'}
          </div>
        </>
      )}
    </motion.div>
  )
}
