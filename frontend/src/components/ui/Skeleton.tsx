export default function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`rounded-lg bg-gradient-to-r from-transparent via-indigo-500/5 to-transparent bg-[length:200%_100%] animate-shimmer ${className}`} />
}

export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-3">
      <div className="flex justify-between"><Skeleton className="h-4 w-3/4" /><Skeleton className="h-5 w-16 rounded-full" /></div>
      <Skeleton className="h-3 w-full" />
      <Skeleton className="h-3 w-2/3" />
      <div className="flex justify-between"><Skeleton className="h-3 w-20" /><Skeleton className="h-3 w-16" /></div>
    </div>
  )
}

export function BriefSkeleton() {
  return (
    <div className="space-y-4">
      <div className="flex justify-between"><Skeleton className="h-6 w-40" /><Skeleton className="h-6 w-20 rounded-full" /></div>
      <Skeleton className="h-10 w-full rounded-lg" />
      <Skeleton className="h-12 w-full rounded-lg" />
      {[1,2,3].map(i => <CardSkeleton key={i} />)}
    </div>
  )
}
