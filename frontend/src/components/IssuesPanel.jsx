import { motion } from 'framer-motion'

const ITEM = {
  hidden: { opacity: 0, x: -16 },
  show: { opacity: 1, x: 0 },
}

export default function IssuesPanel({ issues = [] }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.15 }}
      className="glass-card rounded-3xl p-6 flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl bg-red-500/15 border border-red-500/20">
          ⚠️
        </div>
        <div>
          <h3 className="text-white font-bold text-base">Code Issues</h3>
          <p className="text-slate-500 text-xs mt-0.5">
            {issues.length} problem{issues.length !== 1 ? 's' : ''} found in your repos
          </p>
        </div>
      </div>

      {issues.length === 0 ? (
        <div className="flex-1 flex items-center justify-center py-8">
          <p className="text-emerald-400 text-sm">✅ No critical issues found!</p>
        </div>
      ) : (
        <div className="space-y-4 flex-1 overflow-y-auto max-h-[520px] pr-1">
          {issues.map((issue, i) => (
            <motion.div
              key={i}
              variants={ITEM}
              whileHover={{ x: 4, transition: { duration: 0.15 } }}
              className="group bg-white/[0.015] border border-white/5 rounded-2xl p-4 cursor-default hover:border-red-500/20 hover:bg-red-500/[0.025] transition-colors duration-200"
            >
              <div className="flex items-start gap-3">
                {/* Index dot */}
                <div className="w-6 h-6 rounded-full bg-red-500/20 border border-red-500/30 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-red-400 text-[10px] font-bold">{i + 1}</span>
                </div>

                <div className="flex-1 min-w-0">
                  {/* Filename */}
                  <p className="text-slate-500 text-[11px] font-mono mb-1.5 truncate">
                    📁 {issue.file}
                  </p>
                  {/* Problem */}
                  <p className="text-slate-200 text-sm font-medium leading-snug mb-3">
                    {issue.problem}
                  </p>
                  {/* Fix */}
                  <div className="bg-emerald-500/8 border border-emerald-500/20 rounded-xl px-3 py-2.5">
                    <p className="text-emerald-300 text-xs leading-relaxed">
                      <span className="font-bold text-emerald-400">Fix → </span>
                      {issue.fix}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  )
}
