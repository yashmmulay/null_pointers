import { motion } from 'framer-motion';

export default function MarketAnalysis({ percentile, salaryGap }) {
  if (!percentile) return null;
  
  return (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card glow-blue rounded-3xl p-8 shadow-xl h-full flex flex-col"
    >
        <div className="flex items-center gap-3 mb-8">
            <span className="text-2xl bg-blue-500/20 p-2 rounded-lg">🏅</span>
            <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
                Market Standing
            </h2>
        </div>
        
        <div className="space-y-6 flex-grow">
          <div className="bg-white/[0.03] border border-white/5 rounded-2xl p-6 relative overflow-hidden transition-all hover:bg-white/[0.05]">
             <h3 className="text-slate-400 text-sm font-semibold tracking-wide uppercase mb-3">Percentile Ranking</h3>
             <p className="text-2xl font-bold text-white relative z-10">{percentile}</p>
             <div className="absolute -right-4 -bottom-4 opacity-5 text-9xl pointer-events-none">🎯</div>
          </div>
          
          <div className="bg-white/[0.03] border border-white/5 rounded-2xl p-6 relative overflow-hidden transition-all hover:bg-white/[0.05]">
             <h3 className="text-slate-400 text-sm font-semibold tracking-wide uppercase mb-3">Salary Bracket Gap</h3>
             <p className="text-[15px] text-slate-300 leading-relaxed relative z-10">{salaryGap}</p>
             <div className="absolute -right-4 -bottom-8 opacity-5 text-9xl pointer-events-none">📈</div>
          </div>
        </div>
    </motion.div>
  );
}
