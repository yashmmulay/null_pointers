import { motion } from 'framer-motion'

const VERDICT_CONFIG = {
  Junior: {
    gradient: 'from-orange-400 via-amber-400 to-red-400',
    glow:     'glow-orange',
    border:   'border-orange-500/25',
    bg:       'bg-orange-500/5',
    emoji:    '🌱',
    label:    'Junior Developer',
    tagline:  'Solid foundation with significant growth ahead.',
    badge:    { text: 'Entry Level', color: 'text-orange-300 bg-orange-500/10 border-orange-500/20' },
  },
  Mid: {
    gradient: 'from-blue-400 via-indigo-400 to-violet-400',
    glow:     'glow-purple',
    border:   'border-violet-500/25',
    bg:       'bg-violet-500/5',
    emoji:    '⚡',
    label:    'Mid-Level Developer',
    tagline:  'Good technical foundation. Ready for complex systems.',
    badge:    { text: 'Mid Level', color: 'text-violet-300 bg-violet-500/10 border-violet-500/20' },
  },
  Senior: {
    gradient: 'from-emerald-400 via-teal-400 to-cyan-400',
    glow:     'glow-cyan',
    border:   'border-emerald-500/25',
    bg:       'bg-emerald-500/5',
    emoji:    '🏆',
    label:    'Senior Developer',
    tagline:  'High-quality, production-ready mindset demonstrated.',
    badge:    { text: 'Senior Level', color: 'text-emerald-300 bg-emerald-500/10 border-emerald-500/20' },
  },
}

export default function SkillVerdict({ verdict }) {
  const cfg = VERDICT_CONFIG[verdict] ?? VERDICT_CONFIG['Mid']

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.92, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 180, damping: 22, delay: 0.1 }}
      className={`glass-card ${cfg.glow} ${cfg.border} ${cfg.bg} rounded-3xl p-12 text-center`}
    >
      {/* Label */}
      <p className="text-slate-500 text-xs uppercase tracking-[0.2em] font-semibold mb-6">
        AI Skill Verdict
      </p>

      {/* Emoji */}
      <motion.div
        initial={{ scale: 0, rotate: -20 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: 'spring', stiffness: 260, damping: 18, delay: 0.35 }}
        className="text-7xl mb-6"
      >
        {cfg.emoji}
      </motion.div>

      {/* Verdict text */}
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className={`text-5xl md:text-6xl font-black bg-gradient-to-r ${cfg.gradient} bg-clip-text text-transparent`}
      >
        {cfg.label}
      </motion.h2>

      <p className="text-slate-400 mt-3 text-base">{cfg.tagline}</p>

      {/* Badge */}
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.65 }}
        className={`inline-block mt-5 px-4 py-1.5 rounded-full border text-xs font-bold uppercase tracking-wider ${cfg.badge.color}`}
      >
        {cfg.badge.text}
      </motion.span>
    </motion.div>
  )
}
