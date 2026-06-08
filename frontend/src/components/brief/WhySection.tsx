import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown } from 'lucide-react'

export default function WhySection({ reasons }: { reasons: string[] }) {
  const [open, setOpen] = useState(false)
  if (!reasons?.length) return null
  return (
    <div className="border-t border-gray-200 dark:border-gray-800 pt-2 mt-2">
      <button onClick={() => setOpen(!open)} className="flex items-center gap-1 text-xs font-medium text-indigo-500 hover:text-indigo-400 transition-colors">
        <span>🧠 Why does this matter?</span>
        <motion.span animate={{ rotate: open ? 180 : 0 }}><ChevronDown size={14} /></motion.span>
      </button>
      <AnimatePresence>
        {open && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <ul className="mt-2 space-y-1">
              {reasons.map((r, i) => (
                <li key={i} className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed flex gap-2">
                  <span className="text-indigo-500 mt-0.5">→</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
