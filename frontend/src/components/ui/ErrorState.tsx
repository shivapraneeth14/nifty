import { motion } from 'framer-motion'

export default function ErrorState({ message = 'Something went wrong', onRetry }: { message?: string; onRetry?: () => void }) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col items-center justify-center py-20 text-center px-4">
      <div className="text-4xl mb-4">⚠️</div>
      <p className="text-gray-500 dark:text-gray-400 text-sm mb-4">{message}</p>
      {onRetry && <button onClick={onRetry} className="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-500/90 transition-colors">Try again</button>}
    </motion.div>
  )
}

export function EmptyState({ icon = '📭', message = 'Nothing here yet', submessage }: { icon?: string; message?: string; submessage?: string }) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col items-center justify-center py-20 text-center px-4">
      <div className="text-5xl mb-4">{icon}</div>
      <p className="text-gray-900 dark:text-gray-100 font-medium mb-1">{message}</p>
      {submessage && <p className="text-gray-400 dark:text-gray-500 text-sm">{submessage}</p>}
    </motion.div>
  )
}
