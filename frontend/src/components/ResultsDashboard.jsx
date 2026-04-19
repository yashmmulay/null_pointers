import { motion } from 'framer-motion'
import SkillVerdict from './SkillVerdict'
import IssuesPanel from './IssuesPanel'
import ResumeAnalysis from './ResumeAnalysis'
import DamagingProjects from './DamagingProjects'
import Roadmap from './Roadmap'
import MarketAnalysis from './MarketAnalysis'
import JobMatches from './JobMatches'
import UIAuditPanel from './UIAuditPanel'
import LiveAppMetrics from './LiveAppMetrics'

const STAGGER = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
}

export default function ResultsDashboard({ data }) {
  const { username, repos_analyzed = [], live_app_metrics, analysis } = data
  const totalFiles = repos_analyzed.reduce((sum, repo) => sum + (repo.files_analyzed ?? 0), 0)

  // Condition to show UI/UX section: 
  // 1. Manually provided URL
  // 2. Or discovered homepage URL in repo metadata
  const hasLiveLink = live_app_metrics && live_app_metrics.url_audited && live_app_metrics.url_audited !== "Not provided";

  return (
    <motion.section
      variants={STAGGER}
      initial="hidden"
      animate="show"
      className="max-w-6xl mx-auto px-6 pb-28"
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <p className="text-slate-500 text-sm tracking-widest uppercase mb-2">
          Audit Complete
        </p>
        <h2 className="text-4xl font-black text-white">@{username}</h2>
        <p className="text-slate-500 text-sm mt-2">
          {repos_analyzed.length} repos · {totalFiles} files analyzed
        </p>

        <div className="flex flex-wrap justify-center gap-2 mt-5">
          {repos_analyzed.map((repo, index) => (
            <a
              key={index}
              href={repo.url}
              target="_blank"
              rel="noreferrer"
              className="px-3 py-1 glass-card rounded-full text-xs text-slate-400 hover:text-white hover:border-violet-500/30 transition-colors duration-200"
            >
              {repo.name} · {repo.language} · star {repo.stars}
            </a>
          ))}
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <SkillVerdict verdict={analysis.skill_verdict} />
        <MarketAnalysis percentile={analysis.percentile_ranking} salaryGap={analysis.salary_bracket_gap} />
      </div>

      {analysis.ats_score && analysis.ats_score.score !== undefined && analysis.ats_score.score !== null && (
        <div className="mt-6">
          <ResumeAnalysis atsData={analysis.ats_score} />
        </div>
      )}

      {hasLiveLink && (
        <>
          <div className="mt-6">
            <LiveAppMetrics metrics={data.live_app_metrics} />
          </div>
          {analysis.ui_ux_feedback && analysis.ui_ux_feedback.length > 0 && (
            <div className="mt-6">
              <UIAuditPanel feedback={analysis.ui_ux_feedback} />
            </div>
          )}
        </>
      )}

      <div className="mt-6">
        <JobMatches matches={analysis.job_matches} />
      </div>

      <div className="mt-6">
        <IssuesPanel issues={analysis.issues} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <DamagingProjects projects={analysis.damaging_projects || []} />
        <Roadmap roadmap={analysis.roadmap || []} />
      </div>
    </motion.section>
  )
}
