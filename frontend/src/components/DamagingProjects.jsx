import { motion } from 'framer-motion'

export default function DamagingProjects({ projects = [] }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.25 }}
      className="glass-card rounded-3xl p-6"
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl bg-red-500/15 border border-red-500/20">
          🔥
        </div>
        <div>
          <h3 className="text-white font-bold text-base">Damaging Projects</h3>
          <p className="text-slate-500 text-xs mt-0.5">
            These repos may hurt your job applications
          </p>
        </div>
      </div>

      {projects.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-emerald-500/6 border border-emerald-500/20 rounded-2xl p-6 text-center"
        >
          <p className="text-2xl mb-2">🎉</p>
          <p className="text-emerald-400 font-semibold text-sm">No damaging projects found.</p>
          <p className="text-slate-500 text-xs mt-1">Clean portfolio — keep it that way.</p>
        </motion.div>
      ) : (
        <div className="space-y-3">
          {projects.map((project, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * i + 0.3 }}
              whileHover={{ x: 4, transition: { duration: 0.15 } }}
              className="group bg-red-500/5 border border-red-500/20 rounded-2xl p-4 cursor-default hover:border-red-500/35 hover:bg-red-500/8 transition-all duration-200"
              style={{ boxShadow: '0 0 12px rgba(239, 68, 68, 0.04)' }}
            >
              <div className="flex items-start gap-3">
                <span className="text-red-400 flex-shrink-0 text-lg mt-0.5">⚡</span>
                <div>
                  <p className="text-red-300 font-mono font-semibold text-sm mb-1">
                    {project.repo}
                  </p>
                  <p className="text-slate-400 text-xs leading-relaxed">
                    {project.reason}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}

          <p className="text-slate-600 text-xs text-center mt-4">
            💡 Consider archiving or improving these before job hunting.
          </p>
        </div>
      )}
    </motion.div>
  )
}
