import { motion } from 'framer-motion'

export default function Hero() {
  return (
    <section className="relative min-h-[58vh] flex flex-col items-center justify-center px-6 pt-20 pb-12 overflow-hidden">
      <div
        className="orb absolute top-[10%] left-[15%] w-[420px] h-[420px] opacity-20"
        style={{ background: 'radial-gradient(circle, #6366f1, transparent)' }}
      />
      <div
        className="orb absolute bottom-[5%] right-[10%] w-[340px] h-[340px] opacity-15"
        style={{
          background: 'radial-gradient(circle, #06b6d4, transparent)',
          animationDelay: '2.5s',
        }}
      />
      <div
        className="orb absolute top-[40%] right-[25%] w-[260px] h-[260px] opacity-10"
        style={{
          background: 'radial-gradient(circle, #8b5cf6, transparent)',
          animationDelay: '1.2s',
        }}
      />

      <div className="grid-bg absolute inset-0 pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: 'easeOut' }}
        className="relative z-10 text-center max-w-4xl mx-auto"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full border border-violet-500/30 bg-violet-500/5 text-violet-300 text-xs font-semibold tracking-widest uppercase"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
          AI Powered · Real Code · Resume Extraction
        </motion.div>

        <h1 className="text-5xl sm:text-6xl md:text-7xl font-black leading-[1.05] tracking-tight mb-6">
          <span className="text-white">Developer </span>
          <span className="gradient-text">Career Intel</span>
          <br />
          <span className="text-white">System</span>
        </h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.45, duration: 0.6 }}
          className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed"
        >
          Audit actual GitHub code, auto-extract your profile from a resume PDF, and get a tighter ATS score,
          live app metrics, and a focused 90-day roadmap.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.65, duration: 0.5 }}
          className="mt-10 flex flex-wrap justify-center gap-3"
        >
          {[
            { icon: 'CC', label: 'Radon Complexity', color: 'text-yellow-400 border-yellow-500/20 bg-yellow-500/5' },
            { icon: 'SEC', label: 'Bandit Security', color: 'text-red-400 border-red-500/20 bg-red-500/5' },
            { icon: 'AI', label: 'Gemini Review', color: 'text-cyan-400 border-cyan-500/20 bg-cyan-500/5' },
            { icon: 'ATS', label: 'ATS Scoring', color: 'text-blue-400 border-blue-500/20 bg-blue-500/5' },
            { icon: 'URL', label: 'Live Metrics', color: 'text-violet-400 border-violet-500/20 bg-violet-500/5' },
          ].map(({ icon, label, color }) => (
            <span
              key={label}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-medium ${color}`}
            >
              {icon} {label}
            </span>
          ))}
        </motion.div>
      </motion.div>
    </section>
  )
}
