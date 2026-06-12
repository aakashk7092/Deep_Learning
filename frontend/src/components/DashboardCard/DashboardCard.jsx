import { motion } from 'framer-motion'

export default function DashboardCard({ title, value, icon: Icon, tone = 'from-canopy to-leaf', caption }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="card overflow-hidden"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-300">{title}</p>
          <p className="mt-3 text-3xl font-bold">{value}</p>
          {caption && <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">{caption}</p>}
        </div>
        {Icon && (
          <div className={`grid h-12 w-12 place-items-center rounded-lg bg-gradient-to-br ${tone} text-white shadow-glow`}>
            <Icon />
          </div>
        )}
      </div>
    </motion.article>
  )
}
