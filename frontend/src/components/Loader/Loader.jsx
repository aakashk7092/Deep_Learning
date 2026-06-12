import { motion } from 'framer-motion'

export default function Loader({ label = 'Loading intelligence...' }) {
  return (
    <div className="flex min-h-44 flex-col items-center justify-center gap-4 text-center">
      <div className="relative h-16 w-16">
        {[0, 1, 2].map((item) => (
          <motion.span
            key={item}
            className="absolute inset-0 rounded-full border-2 border-canopy/30"
            animate={{ scale: [0.45, 1.05, 0.45], opacity: [0.8, 0.2, 0.8] }}
            transition={{ duration: 1.8, repeat: Infinity, delay: item * 0.25 }}
          />
        ))}
        <div className="absolute inset-4 rounded-full bg-gradient-to-br from-leaf to-canopy" />
      </div>
      <p className="text-sm font-medium text-slate-500 dark:text-slate-300">{label}</p>
    </div>
  )
}
