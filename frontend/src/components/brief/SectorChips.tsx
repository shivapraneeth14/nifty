export default function SectorChips({ sectors }: { sectors: Record<string, string> }) {
  if (!sectors || !Object.keys(sectors).length) return null
  return (
    <div className="flex flex-wrap gap-1.5 mt-2">
      {Object.entries(sectors).map(([sector, impact]) => (
        <span key={sector} className={`inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded-full border ${
          impact.includes('⭐') ? 'bg-green-500/10 text-green-600 dark:text-green-400 border-green-500/20' :
          impact.includes('✅') ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20' :
          'bg-gray-500/10 text-gray-500 border-gray-500/20'
        }`}>
          {sector}
        </span>
      ))}
    </div>
  )
}
