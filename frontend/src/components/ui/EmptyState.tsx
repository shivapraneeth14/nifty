import { motion } from 'framer-motion'

interface Props {
  icon?: string
  message?: string
  submessage?: string
}

export default function EmptyState({ icon = '📭', message = 'Nothing here yet', submessage }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center py-20 text-center px-4"
    >
      <div className="text-5xl mb-4">{icon}</div>
      <p className="text-text-primary font-medium mb-1">{message}</p>
      {submessage && <p className="text-text-secondary text-sm">{submessage}</p>}
    </motion.div>
  )
}
