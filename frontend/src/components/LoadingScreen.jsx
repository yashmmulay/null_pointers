import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

const STEPS = [
  { icon: 'PDF', label: 'Preparing repositories and resume context...' },
  { icon: 'SRC', label: 'Reading real code files for evidence...' },
  { icon: 'CC', label: 'Running complexity and maintainability analysis...' },
  { icon: 'SEC', label: 'Scanning for security and lint issues...' },
  { icon: 'UI', label: 'Collecting live app metrics when a URL is provided...' },
  { icon: 'AI', label: 'Gemini is generating the career and ATS report...' },
  { icon: 'OK', label: 'Finalizing charts, feedback, and roadmap...' },
]

export default function LoadingScreen() {
  const [step, setStep] = useState(0)

  useEffect(() => {
    const id = setInterval(() => {
      setStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev))
    }, 3500)
    return () => clearInterval(id)
  }, [])

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
      className="max-w-xl mx-auto px-6 pb-24"
    >
      <div
        className="glass-card rounded-3xl p-10 text-center"
        style={{ boxShadow: '0 0 60px rgba(139, 92, 246, 0.15)' }}
      >
        <motion.div
          key={step}
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          className="w-16 h-16 mx-auto mb-5 rounded-2xl flex items-center justify-center text-lg font-black tracking-wider"
          style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)' }}
        >
          {STEPS[step].icon}
        </motion.div>

        <motion.h3
          key={`label-${step}`}
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-white font-semibold text-base mb-1"
        >
          {STEPS[step].label}
        </motion.h3>
        <p className="text-slate-500 text-xs mb-8">
          Reading real repositories and resume text. This usually takes 20-45 seconds.
        </p>

        <div className="space-y-2.5 text-left">
          {STEPS.map((item, index) => {
            const done = index < step
            const active = index === step
            const pending = index > step

            return (
              <div key={index} className="flex items-center gap-3">
                <div
                  className={`
                    w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0
                    transition-all duration-500
                    ${done ? 'bg-emerald-500 text-white' : ''}
                    ${active ? 'bg-violet-500 text-white animate-pulse' : ''}
                    ${pending ? 'bg-white/10 text-transparent' : ''}
                  `}
                >
                  {done ? 'Y' : index + 1}
                </div>

                <span
                  className={`text-xs transition-colors duration-500 ${
                    done
                      ? 'text-emerald-400 line-through decoration-emerald-400/40'
                      : active
                        ? 'text-white font-medium'
                        : 'text-slate-600'
                  }`}
                >
                  {item.label}
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </motion.section>
  )
}
