import { motion } from 'framer-motion'

export default function Toggle({ options, selected, onChange }: { options: { label: string; value: string }[]; selected: string; onChange: (v: string) => void }) {
  const idx = options.findIndex(o => o.value === selected)
  return (
    <div className="flex bg-gray-50 dark:bg-[#131620] rounded-xl p-1 border border-gray-200 dark:border-gray-800 relative">
      <motion.div layout transition={{ type: 'spring', stiffness: 400, damping: 30 }}
        className="absolute inset-y-1 bg-white dark:bg-[#1A1D28] border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm"
        style={{ left: `calc(${idx} * (100% / ${options.length}) + 4px)`, width: `calc((100% / ${options.length}) - 8px)` }}
      />
      {options.map(opt => (
        <button key={opt.value} onClick={() => onChange(opt.value)}
          className={`flex-1 relative z-10 py-1.5 text-sm font-medium transition-colors rounded-lg ${selected === opt.value ? 'text-gray-900 dark:text-gray-100' : 'text-gray-400 dark:text-gray-500 hover:text-gray-900 dark:hover:text-gray-100'}`}
        >{opt.label}</button>
      ))}
    </div>
  )
}
