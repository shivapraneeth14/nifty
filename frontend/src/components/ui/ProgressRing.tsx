import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

export default function ProgressRing({ value, size = 80, strokeWidth = 6, label }: { value: number; size?: number; strokeWidth?: number; label?: string }) {
  const [progress, setProgress] = useState(0)
  const r = (size - strokeWidth) / 2
  const circ = 2 * Math.PI * r
  const offset = circ - (progress / 100) * circ
  const color = value >= 70 ? '#22C55E' : value >= 50 ? '#F59E0B' : '#EF4444'
  useEffect(() => { const t = setTimeout(() => setProgress(Math.min(value, 100)), 100); return () => clearTimeout(t) }, [value])

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="currentColor" strokeWidth={strokeWidth} className="text-gray-200 dark:text-gray-800" />
        <motion.circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round"
          strokeDasharray={circ} initial={{ strokeDashoffset: circ }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: 'easeOut' }} />
      </svg>
      <div className="relative" style={{ width: size, height: size }}>
        <span className="absolute inset-0 flex items-center justify-center text-lg font-bold font-mono" style={{ color }}>{value}%</span>
      </div>
      {label && <span className="text-xs text-gray-400 dark:text-gray-500">{label}</span>}
    </div>
  )
}
