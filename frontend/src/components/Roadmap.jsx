import { motion } from 'framer-motion'

const DOT_GRADIENTS = [
  { from: '#6366f1', to: '#818cf8' },
  { from: '#8b5cf6', to: '#a78bfa' },
  { from: '#06b6d4', to: '#67e8f9' },
  { from: '#10b981', to: '#6ee7b7' },
]

function normalizeRoadmap(roadmap) {
  if (!Array.isArray(roadmap)) {
    return []
  }

  return roadmap
    .map((item, index) => {
      if (!item || typeof item !== 'object') {
        return null
      }

      const label =
        item.phase ||
        item.week ||
        item.title ||
        `Phase ${index + 1}`

      const focus =
        item.focus ||
        item.goal ||
        item.description ||
        ''

      if (!String(focus).trim()) {
        return null
      }

      return {
        label: String(label).trim(),
        focus: String(focus).trim(),
      }
    })
    .filter(Boolean)
}

export default function Roadmap({ roadmap = [] }) {
  const items = normalizeRoadmap(roadmap)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="glass-card rounded-3xl p-6"
    >
      <div className="flex items-center gap-3 mb-7">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl bg-cyan-500/15 border border-cyan-500/20">
          90
        </div>
        <div>
          <h3 className="text-white font-bold text-base">High-Impact Career Roadmap</h3>
          <p className="text-slate-500 text-xs mt-0.5">
            90-Day Execution Plan
          </p>
        </div>
      </div>

      {items.length === 0 ? (
        <p className="text-slate-500 text-sm text-center py-6">No roadmap generated yet.</p>
      ) : (
        <div className="relative">
          <div className="timeline-line absolute left-[18px] top-4 bottom-4 w-0.5 rounded-full" />

          <div className="space-y-5">
            {items.map((item, index) => {
              const gradient = DOT_GRADIENTS[index % DOT_GRADIENTS.length]
              return (
                <motion.div
                  key={`${item.label}-${index}`}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * index + 0.35 }}
                  whileHover={{ x: 5, transition: { duration: 0.15 } }}
                  className="flex items-start gap-4 cursor-default"
                >
                  <div
                    className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0 relative z-10"
                    style={{
                      background: `linear-gradient(135deg, ${gradient.from}, ${gradient.to})`,
                      boxShadow: `0 0 16px ${gradient.from}55`,
                    }}
                  >
                    {index + 1}
                  </div>

                  <div className="flex-1 bg-white/[0.018] border border-white/6 rounded-2xl px-4 py-3.5 hover:border-white/10 transition-colors duration-200">
                    <p
                      className="text-[10px] font-bold uppercase tracking-widest mb-1"
                      style={{ color: gradient.from }}
                    >
                      {item.label}
                    </p>
                    <p className="text-slate-200 text-sm leading-relaxed">
                      {item.focus}
                    </p>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      )}
    </motion.div>
  )
}
