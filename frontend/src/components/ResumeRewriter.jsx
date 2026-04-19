import { motion } from 'framer-motion'

export default function ResumeRewriter({ resumeData }) {
  if (!resumeData) return null
  const { before, after } = resumeData

  const copyAfter = () => {
    navigator.clipboard?.writeText(after).catch(() => {})
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-card rounded-3xl p-6 flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl bg-violet-500/15 border border-violet-500/20">
          ✍️
        </div>
        <div>
          <h3 className="text-white font-bold text-base">Resume Rewriter</h3>
          <p className="text-slate-500 text-xs mt-0.5">
            Strengthened based on your actual code quality
          </p>
        </div>
      </div>

      <div className="flex-1 space-y-4">
        {/* BEFORE */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 rounded-full bg-red-400 flex-shrink-0" />
            <span className="text-red-400 text-[11px] font-bold uppercase tracking-[0.15em]">
              Before
            </span>
          </div>
          <div className="bg-red-500/5 border border-red-500/20 rounded-2xl p-4">
            <p className="text-slate-300 text-sm leading-relaxed italic">
              "{before}"
            </p>
          </div>
        </div>

        {/* Animated arrow */}
        <div className="flex justify-center">
          <motion.div
            animate={{ y: [0, 5, 0] }}
            transition={{ repeat: Infinity, duration: 1.6, ease: 'easeInOut' }}
            className="text-slate-600 text-xl select-none"
          >
            ↓
          </motion.div>
        </div>

        {/* AFTER */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 flex-shrink-0" />
              <span className="text-emerald-400 text-[11px] font-bold uppercase tracking-[0.15em]">
                After (AI Rewrite)
              </span>
            </div>
            <button
              onClick={copyAfter}
              title="Copy to clipboard"
              className="text-slate-600 hover:text-slate-300 transition-colors text-xs px-2 py-1 rounded-md hover:bg-white/5"
            >
              📋 Copy
            </button>
          </div>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="bg-emerald-500/6 border border-emerald-500/25 rounded-2xl p-4"
            style={{ boxShadow: '0 0 20px rgba(16, 185, 129, 0.08)' }}
          >
            <p className="text-emerald-100 text-sm leading-relaxed font-medium">
              "{after}"
            </p>
          </motion.div>

          <p className="text-slate-600 text-xs mt-3 text-center">
            ✦ Rewritten using evidence from your actual GitHub code
          </p>
        </div>
      </div>
    </motion.div>
  )
}
