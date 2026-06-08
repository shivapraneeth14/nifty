import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import type { OptionChain } from '../../types/brief'
import { fetchOptionChain } from '../../services/options'

export default function OptionChainCard() {
  const [data, setData] = useState<OptionChain | null>(null)

  useEffect(() => { fetchOptionChain().then(setData).catch(() => {}) }, [])

  if (!data) return null

  const pcrColor = data.pcr_volume != null
    ? data.pcr_volume > 1.2 ? 'text-red-500' : data.pcr_volume < 0.8 ? 'text-green-500' : 'text-amber-500'
    : ''

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Options Chain</h3>
        {data.expiry && <span className="text-[10px] text-gray-400">Exp: {data.expiry}</span>}
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-[10px] text-gray-400 dark:text-gray-500">PCR (Volume)</div>
          <div className={`text-sm font-bold font-mono ${pcrColor}`}>{data.pcr_volume?.toFixed(2) ?? '—'}</div>
        </div>
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-[10px] text-gray-400 dark:text-gray-500">PCR (OI)</div>
          <div className={`text-sm font-bold font-mono ${pcrColor}`}>{data.pcr_oi?.toFixed(2) ?? '—'}</div>
        </div>
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-[10px] text-gray-400 dark:text-gray-500">Max Pain</div>
          <div className="text-sm font-bold font-mono text-gray-900 dark:text-gray-100">{data.max_pain != null ? data.max_pain.toLocaleString() : '—'}</div>
        </div>
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-[10px] text-gray-400 dark:text-gray-500">OI Ratio</div>
          <div className="text-sm font-bold font-mono text-gray-900 dark:text-gray-100">{data.pcr_oi != null ? (data.pcr_oi > 1 ? 'Puts > Calls' : 'Calls > Puts') : '—'}</div>
        </div>
      </div>
      {data.interpretation && (
        <p className="text-[10px] text-gray-500 dark:text-gray-400 leading-relaxed">{data.interpretation}</p>
      )}
    </motion.div>
  )
}
