import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, AlertCircle, X } from 'lucide-react'

interface ToastItem {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

interface ToastContextType { toast: (message: string, type?: 'success' | 'error' | 'info') => void }

const ToastContext = createContext<ToastContextType>({ toast: () => {} })

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([])
  const toast = useCallback((message: string, type: 'success' | 'error' | 'info' = 'info') => {
    const id = Date.now()
    setItems((prev) => [...prev, { id, message, type }])
    setTimeout(() => setItems((prev) => prev.filter((i) => i.id !== id)), 3000)
  }, [])

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-2 w-[90%] max-w-sm">
        <AnimatePresence>
          {items.map((item) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              className={`flex items-center gap-2 px-4 py-3 rounded-xl shadow-lg border text-sm font-medium backdrop-blur-xl ${
                item.type === 'success' ? 'bg-green-500/10 border-green-500/20 text-green-600 dark:text-green-400' :
                item.type === 'error' ? 'bg-red-500/10 border-red-500/20 text-red-600 dark:text-red-400' :
                'bg-indigo-500/10 border-indigo-500/20 text-indigo-500'
              }`}
            >
              {item.type === 'success' ? <CheckCircle size={16} /> : item.type === 'error' ? <AlertCircle size={16} /> : null}
              <span className="flex-1">{item.message}</span>
              <button onClick={() => setItems((prev) => prev.filter((i) => i.id !== item.id))}><X size={14} /></button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  )
}

export const useToast = () => useContext(ToastContext)
