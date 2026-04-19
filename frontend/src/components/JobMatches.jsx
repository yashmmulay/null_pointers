import { motion } from "framer-motion";

export default function JobMatches({ matches }) {
    if (!matches || matches.length === 0) return null;

    const getLink = (platform, role, type) => {
        const keyword = encodeURIComponent(role);
        const keywordWithRemote = encodeURIComponent(`${role} ${type === 'Remote' ? 'Remote' : ''}`.trim());

        switch (platform) {
            case 'linkedin':
                return `https://www.linkedin.com/jobs/search/?keywords=${keywordWithRemote}`;
            case 'naukri':
                return `https://www.naukri.com/${role.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-jobs?k=${keyword}`;
            case 'jooble':
                return `https://jooble.org/SearchResult?ukw=${keywordWithRemote}`;
            case 'internshala':
                return `https://internshala.com/internships/keywords-${role.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`;
            default:
                return '#';
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card glow-emerald rounded-3xl p-8"
        >
            <div className="flex items-center gap-3 mb-6">
                <span className="text-2xl bg-emerald-500/20 p-2 rounded-lg">💼</span>
                <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-400">
                    Live Job Search Matches
                </h2>
            </div>
            
            <div className="space-y-6">
                {matches.map((job, idx) => (
                    <motion.div
                        key={idx}
                        className="bg-white/[0.02] hover:bg-white/[0.05] transition-all duration-300 border border-white/10 rounded-xl p-5 flex flex-col gap-4"
                    >
                        <div className="flex gap-4 items-start">
                            <div className="text-3xl mt-0.5 opacity-60">🏢</div>
                            <div>
                               <h3 className="text-lg font-bold text-emerald-300">{job.role}</h3>
                               <p className="text-sm text-slate-300 font-medium mt-1 mb-3">{job.companies}</p>
                               <span className="inline-block px-3 py-1 rounded-full bg-teal-500/20 border border-teal-500/30 text-teal-300 text-xs font-semibold uppercase tracking-wider">
                                   {job.type}
                               </span>
                            </div>
                        </div>

                        {/* Smart Deep Links */}
                        <div className="flex flex-wrap gap-3 pt-4 border-t border-white/5">
                            <a href={getLink('linkedin', job.role, job.type)} target="_blank" rel="noreferrer" className="text-[10px] font-bold tracking-widest px-4 py-2 rounded-md bg-blue-600/10 hover:bg-blue-600/30 text-blue-400 border border-blue-500/20 transition-colors uppercase">
                                ↳ LinkedIn
                            </a>
                            <a href={getLink('naukri', job.role, job.type)} target="_blank" rel="noreferrer" className="text-[10px] font-bold tracking-widest px-4 py-2 rounded-md bg-orange-600/10 hover:bg-orange-600/30 text-orange-400 border border-orange-500/20 transition-colors uppercase">
                                ↳ Naukri
                            </a>
                            <a href={getLink('jooble', job.role, job.type)} target="_blank" rel="noreferrer" className="text-[10px] font-bold tracking-widest px-4 py-2 rounded-md bg-indigo-600/10 hover:bg-indigo-600/30 text-indigo-400 border border-indigo-500/20 transition-colors uppercase">
                                ↳ Jooble
                            </a>
                            <a href={getLink('internshala', job.role, job.type)} target="_blank" rel="noreferrer" className="text-[10px] font-bold tracking-widest px-4 py-2 rounded-md bg-sky-600/10 hover:bg-sky-600/30 text-sky-400 border border-sky-500/20 transition-colors uppercase">
                                ↳ Internshala
                            </a>
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}
