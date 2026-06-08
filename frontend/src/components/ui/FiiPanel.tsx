import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import type { Fiidata } from '../../types/brief'
import { fetchFiidata } from '../../services/fii'

export default function FiiPanel() {
  const [data, setData] = useState<Fiidata | null>(null)

  useEffect(() => { fetchFiidata().then(setData).catch(() => {}) }, [])

  if (!data) return null

  const totalFii = data.fii_equity_cr + data.fii_index_fut_cr
  const color = totalFii > 500 ? 'text-green-500' : totalFii < -500 ? 'text-red-500' : 'text-gray-400'

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">FII / DII Flow</h3>
        <span className={`text-sm font-bold font-mono ${color}`}>
          {totalFii > 0 ? '+' : ''}₹{Math.abs(totalFii).toLocaleString('en-IN')}cr
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-gray-400 dark:text-gray-500">FII Equity</div>
          <div className={`font-mono font-semibold ${data.fii_equity_cr > 0 ? 'text-green-500' : data.fii_equity_cr < 0 ? 'text-red-500' : ''}`}>
            {data.fii_equity_cr > 0 ? '+' : ''}₹{data.fii_equity_cr.toLocaleString('en-IN')}cr
          </div>
        </div>
        <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
          <div className="text-gray-400 dark:text-gray-500">DII Equity</div>
          <div className={`font-mono font-semibold ${data.dii_equity_cr > 0 ? 'text-green-500' : data.dii_equity_cr < 0 ? 'text-red-500' : ''}`}>
            {data.dii_equity_cr > 0 ? '+' : ''}₹{data.dii_equity_cr.toLocaleString('en-IN')}cr
          </div>
        </div>
      </div>
      {data.interpretation && (
        <p className="text-[10px] text-gray-500 dark:text-gray-400 leading-relaxed">{data.interpretation}</p>
      )}
    </motion.div>
  )
}
