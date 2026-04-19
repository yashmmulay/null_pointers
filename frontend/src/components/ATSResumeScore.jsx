import { motion } from 'framer-motion'

function SectionList({ title, items, tone }) {
  if (!items?.length) {
    return null
  }

  const toneMap = {
    add: 'border-emerald-500/20 bg-emerald-500/5 text-emerald-200',
    remove: 'border-red-500/20 bg-red-500/5 text-red-200',
    change: 'border-amber-500/20 bg-amber-500/5 text-amber-100',
  }

  return (
    <div className={`rounded-2xl border p-4 ${toneMap[tone]}`}>
      <p className="text-xs font-bold uppercase tracking-[0.18em] mb-3 opacity-90">{title}</p>
      <div className="space-y-2">
        {items.map((item, index) => (
          <p key={index} className="text-sm leading-relaxed">
            {item}
          </p>
        ))}
      </div>
    </div>
  )
}

export default function ATSResumeScore({ atsScore }) {
  if (!atsScore) {
    return null
  }

  const score = Math.max(0, Math.min(100, Number(atsScore.score) || 0))

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card rounded-3xl p-8"
    >
      <div className="flex items-center justify-between gap-4 mb-6">
        <div>
          <p className="text-slate-500 text-xs uppercase tracking-[0.18em]">ATS Resume Score</p>
          <h3 className="text-white text-xl font-bold mt-2">Resume Screening Readiness</h3>
        </div>
        <div className="relative h-24 w-24 rounded-full border border-cyan-400/20 bg-cyan-400/10 flex items-center justify-center">
          <div
            className="absolute inset-1 rounded-full"
            style={{
              background: `conic-gradient(#22d3ee ${score * 3.6}deg, rgba(255,255,255,0.08) 0deg)`,
            }}
          />
          <div className="relative h-16 w-16 rounded-full bg-[#07070f] flex items-center justify-center text-xl font-black text-cyan-300">
            {score}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <SectionList title="What To Add" items={atsScore.what_to_add} tone="add" />
        <SectionList title="What To Remove" items={atsScore.what_to_remove} tone="remove" />
        <SectionList title="What To Change" items={atsScore.what_to_change} tone="change" />
      </div>
    </motion.div>
  )
}
