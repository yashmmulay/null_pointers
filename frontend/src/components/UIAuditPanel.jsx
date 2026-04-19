import { motion } from 'framer-motion'

export default function UIAuditPanel({ feedback }) {
  if (!feedback || feedback.length === 0) {
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card glow-fuchsia rounded-3xl p-8 col-span-1 lg:col-span-2"
    >
      <div className="flex items-center gap-3 mb-6">
        <span className="text-2xl bg-fuchsia-500/20 p-2 rounded-lg">UI</span>
        <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-400 to-pink-400">
          UI and UX Review
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {feedback.map((item, index) => (
          <div
            key={index}
            className="bg-white/[0.03] hover:bg-white/[0.05] transition-colors border-l-4 border-l-fuchsia-500 border border-white/5 rounded-r-2xl p-6"
          >
            <span className="text-[11px] font-bold uppercase tracking-widest text-fuchsia-400 mb-2 block">
              {item.metric}
            </span>
            <h3 className="text-[15px] text-slate-200 mt-2 font-medium leading-relaxed">
              {item.issue}
            </h3>
            <div className="mt-4 text-sm bg-black/40 border border-white/5 p-4 rounded-xl font-mono text-pink-200/90 leading-normal">
              {item.fix}
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
