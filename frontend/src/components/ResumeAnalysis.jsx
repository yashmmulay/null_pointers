import { motion } from "framer-motion";

export default function ResumeAnalysis({ atsData }) {
    if (!atsData || !atsData.score) return null;

    const getScoreColor = (score) => {
        if (score >= 80) return "text-emerald-400";
        if (score >= 60) return "text-amber-400";
        return "text-red-400";
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card glow-violet rounded-3xl p-8 col-span-1 lg:col-span-2 shadow-xl mt-6"
        >
            <div className="flex flex-col md:flex-row items-center gap-6 mb-8">
                <div className="flex-shrink-0 relative">
                    <svg className="w-32 h-32 transform -rotate-90">
                        <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-white/5" />
                        <circle 
                            cx="64" cy="64" r="56" 
                            stroke="currentColor" 
                            strokeWidth="8" fill="transparent" 
                            strokeDasharray={351.8} 
                            strokeDashoffset={351.8 - (351.8 * atsData.score) / 100}
                            className={`transition-all duration-1000 ease-out ${getScoreColor(atsData.score)}`} 
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className={`text-4xl font-bold mt-1 ${getScoreColor(atsData.score)}`}>{atsData.score}</span>
                        <span className="text-[10px] uppercase tracking-widest text-slate-400">Total</span>
                    </div>
                </div>
                <div>
                     <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-violet-400 to-fuchsia-400 mb-2">
                        ATS Resume Screen
                     </h2>
                     <p className="text-sm text-slate-300 leading-relaxed max-w-2xl">
                         This is how an automated Applicant Tracking System reads your resume before a human ever sees it. Your score is derived from matching measurable evidence, explicit technology footprints, and proper semantic flow.
                     </p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                 {/* What to Add */}
                 <div className="bg-white/[0.03] border border-white/5 p-5 rounded-2xl hover:bg-white/[0.05] transition-colors">
                      <div className="flex items-center gap-2 mb-4">
                           <div className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-sm font-bold">+</div>
                           <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">What to Add</h3>
                      </div>
                      <ul className="space-y-3">
                          {atsData.what_to_add?.map((item, i) => (
                              <li key={i} className="text-sm text-emerald-200/80 leading-relaxed list-disc ml-4">{item}</li>
                          ))}
                      </ul>
                 </div>

                 {/* What to Remove */}
                 <div className="bg-white/[0.03] border border-white/5 p-5 rounded-2xl hover:bg-white/[0.05] transition-colors">
                      <div className="flex items-center gap-2 mb-4">
                           <div className="w-6 h-6 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center text-sm font-bold">-</div>
                           <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">What to Remove</h3>
                      </div>
                      <ul className="space-y-3">
                          {atsData.what_to_remove?.map((item, i) => (
                              <li key={i} className="text-sm text-red-200/80 leading-relaxed list-disc ml-4">{item}</li>
                          ))}
                      </ul>
                 </div>

                 {/* What to Change */}
                 <div className="bg-white/[0.03] border border-white/5 p-5 rounded-2xl hover:bg-white/[0.05] transition-colors">
                      <div className="flex items-center gap-2 mb-4">
                           <div className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center text-sm font-bold">↻</div>
                           <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">What to Change</h3>
                      </div>
                      <ul className="space-y-3">
                          {atsData.what_to_change?.map((item, i) => (
                              <li key={i} className="text-sm text-amber-200/80 leading-relaxed list-disc ml-4">{item}</li>
                          ))}
                      </ul>
                 </div>
            </div>
        </motion.div>
    );
}
