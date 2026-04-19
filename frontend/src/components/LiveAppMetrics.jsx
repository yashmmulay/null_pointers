import { motion } from "framer-motion";

export default function LiveAppMetrics({ metrics }) {
    if (!metrics || !metrics.url_audited || metrics.url_audited === "Not provided") return null;

    const scores = metrics.scores || {};
    const rawMetrics = metrics.metrics || {};
    const isEstimated = !!metrics.estimated;

    const getDialColor = (score) => {
        if (score === "N/A" || score === undefined || score === null) return "text-slate-600";
        if (score >= 90) return "text-emerald-400";
        if (score >= 50) return "text-amber-400";
        return "text-red-400";
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card glow-cyan rounded-3xl p-8 col-span-1 lg:col-span-2 shadow-xl"
        >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
                <div className="flex items-center gap-3">
                    <span className="text-2xl p-2 rounded-lg bg-cyan-500/20">URL</span>
                    <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-400">
                        {isEstimated ? 'Estimated Application Metrics' : 'Live Application Metrics'}
                    </h2>
                </div>
                <div className="text-xs bg-white/[0.04] px-4 py-2 rounded-full border border-white/5 font-mono text-slate-300">
                    Target: <a href={metrics.url_audited} target="_blank" rel="noreferrer" className="text-cyan-400 hover:underline">{metrics.url_audited}</a>
                </div>
            </div>

            {isEstimated && (
                <div className="mb-6 p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-[10px] text-amber-200/80 text-center uppercase tracking-widest">
                    Live Probe Blocked: Showing Repository-Based Score Estimates
                </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="flex flex-col items-center p-4 bg-white/[0.02] rounded-2xl border border-white/5 hover:bg-white/[0.05] transition-colors">
                    <div className={`text-4xl font-bold mb-2 ${getDialColor(scores.performance)}`}>
                        {scores.performance ?? 'N/A'}
                    </div>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center">Performance</span>
                </div>

                <div className="flex flex-col items-center p-4 bg-white/[0.02] rounded-2xl border border-white/5 hover:bg-white/[0.05] transition-colors">
                    <div className={`text-4xl font-bold mb-2 ${getDialColor(scores.accessibility)}`}>
                        {scores.accessibility ?? 'N/A'}
                    </div>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center">Accessibility</span>
                </div>

                <div className="flex flex-col items-center p-4 bg-white/[0.02] rounded-2xl border border-white/5 hover:bg-white/[0.05] transition-colors">
                    <div className={`text-4xl font-bold mb-2 ${getDialColor(scores.best_practices)}`}>
                        {scores.best_practices ?? 'N/A'}
                    </div>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center">Best Practices</span>
                </div>

                <div className="flex flex-col items-center p-4 bg-white/[0.02] rounded-2xl border border-white/5 hover:bg-white/[0.05] transition-colors">
                    <div className={`text-4xl font-bold mb-2 ${getDialColor(scores.seo)}`}>
                        {scores.seo ?? 'N/A'}
                    </div>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest text-center">SEO Score</span>
                </div>
            </div>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-white/5 pt-6">
                <div>
                    <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-1">First Contentful Paint</p>
                    <p className="font-mono text-cyan-200 text-sm">{rawMetrics.first_contentful_paint || "N/A"}</p>
                </div>
                <div>
                    <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-1">Speed Index</p>
                    <p className="font-mono text-cyan-200 text-sm">{rawMetrics.speed_index || "N/A"}</p>
                </div>
                <div>
                    <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-1">Cumulative Layout Shift</p>
                    <div className="font-mono text-cyan-200 text-sm">{rawMetrics.cumulative_layout_shift || "N/A"}</div>
                </div>
            </div>
        </motion.div>
    );
}
