import { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'

import { API_BASE } from '../config'

export default function InputPanel({ onSubmit, loading }) {
  const [username, setUsername] = useState('')
  const [githubToken, setGithubToken] = useState('')
  const [liveUrl, setLiveUrl] = useState('')
  const [resumeFile, setResumeFile] = useState(null)
  const handleSubmit = (event) => {
    event.preventDefault()
    if (!username.trim() || loading) {
      return
    }

    onSubmit(
      username.trim(),
      resumeFile,
      githubToken.trim(),
      liveUrl.trim()
    )
  }

  const canSubmit = username.trim() && !loading

  return (
    <section className="max-w-2xl mx-auto px-6 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="glass-card rounded-3xl p-8 shadow-2xl"
        style={{ boxShadow: '0 0 60px rgba(99, 102, 241, 0.08), inset 0 1px 0 rgba(255,255,255,0.04)' }}
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="github-username"
              className="block text-sm font-semibold text-slate-300 mb-2.5"
            >
              GitHub Username
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-mono text-base select-none">
                @
              </span>
              <input
                id="github-username"
                type="text"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="torvalds"
                required
                autoComplete="off"
                spellCheck="false"
                disabled={loading}
                className="neon-input w-full bg-white/[0.04] border border-white/10 rounded-xl pl-9 pr-4 py-3.5 text-white placeholder-slate-600 transition-all duration-200 disabled:opacity-50 text-sm"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="github-token"
              className="block text-sm font-semibold text-slate-300 mb-2.5"
            >
              GitHub Access Token
              <span className="ml-2 text-xs font-normal text-slate-500">
                (optional - required to analyze private repositories)
              </span>
            </label>
            <input
              id="github-token"
              type="password"
              value={githubToken}
              onChange={(event) => setGithubToken(event.target.value)}
              placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
              autoComplete="off"
              spellCheck="false"
              disabled={loading}
              className="neon-input w-full bg-white/[0.04] border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 transition-all duration-200 disabled:opacity-50 text-sm"
            />
            <p className="mt-1.5 text-xs text-slate-500">
              Only needed if checking private repos. Never saved or logged.
            </p>
          </div>

          <div>
            <label
              htmlFor="resume-file"
              className="block text-sm font-semibold text-slate-300 mb-2.5"
            >
              Resume PDF{' '}
              <span className="text-xs font-normal text-slate-500">
                (optional — we'll scan it with an ATS analyzer)
              </span>
            </label>
            <div className="relative">
              <input
                id="resume-file"
                type="file"
                accept=".pdf,application/pdf"
                onChange={(e) => {
                   if (e.target.files && e.target.files.length > 0) {
                       setResumeFile(e.target.files[0])
                   } else {
                       setResumeFile(null)
                   }
                }}
                disabled={loading}
                className="w-full bg-white/[0.04] border border-white/10 rounded-xl px-4 py-3 text-white file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-500/20 file:text-violet-300 hover:file:bg-violet-500/30 transition-all duration-200 disabled:opacity-50 text-sm"
              />
            </div>
            {resumeFile && (
                <p className="mt-2 text-xs text-emerald-400 font-medium">Selected: {resumeFile.name}</p>
            )}
          </div>

          <div>
            <label
              htmlFor="live-url"
              className="block text-sm font-semibold text-slate-300 mb-2.5"
            >
              Live Application URL
              <span className="ml-2 text-xs font-normal text-slate-500">
                (optional - exposes live PageSpeed metrics in the report)
              </span>
            </label>
            <input
              id="live-url"
              type="url"
              value={liveUrl}
              onChange={(event) => setLiveUrl(event.target.value)}
              placeholder="https://my-live-app.vercel.app"
              autoComplete="off"
              spellCheck="false"
              disabled={loading}
              className="neon-input w-full bg-white/[0.04] border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 transition-all duration-200 disabled:opacity-50 text-sm"
            />
          </div>

          <motion.button
            type="submit"
            disabled={!canSubmit}
            whileHover={canSubmit ? { scale: 1.02 } : {}}
            whileTap={canSubmit ? { scale: 0.97 } : {}}
            className="relative w-full py-4 rounded-xl font-bold text-white text-base overflow-hidden transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
            style={{
              background: loading
                ? 'linear-gradient(135deg, #374151, #1f2937)'
                : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)',
              backgroundSize: '200% 200%',
              boxShadow: loading ? 'none' : '0 0 40px rgba(99, 102, 241, 0.4)',
            }}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg
                  className="animate-spin h-5 w-5 text-slate-300"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.37 0 0 5.37 0 12h4z" />
                </svg>
                <span className="text-slate-300">Analyzing... this takes around 30 seconds</span>
              </span>
            ) : (
              'Audit My Career'
            )}
          </motion.button>
        </form>
      </motion.div>
    </section>
  )
}
