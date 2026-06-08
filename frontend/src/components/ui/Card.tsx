import { type ReactNode } from 'react'

interface Props {
  children: ReactNode
  className?: string
  hover?: boolean
  onClick?: () => void
}

export default function Card({ children, className = '', hover = false, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 transition-all duration-200 ${
        hover ? 'hover:shadow-lg hover:shadow-indigo-500/5 hover:border-indigo-500/30 cursor-pointer hover:scale-[1.01]' : ''
      } ${className}`}
    >
      {children}
    </div>
  )
}
