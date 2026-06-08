interface Props {
  children: string
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'ghost'
  disabled?: boolean
  className?: string
}

const variants = {
  primary: 'bg-brand text-white hover:bg-brand/90 shadow-sm shadow-brand/20',
  secondary: 'bg-surface-secondary text-text-primary border border-border hover:bg-border/50',
  ghost: 'text-text-secondary hover:text-text-primary hover:bg-surface-secondary',
}

export default function Button({ children, onClick, variant = 'primary', disabled, className = '' }: Props) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg transition-all duration-200 active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  )
}
