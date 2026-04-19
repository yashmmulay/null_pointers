import { useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import axios from 'axios'

import { API_BASE } from './config'
import Hero from './components/Hero'
import InputPanel from './components/InputPanel'
import LoadingScreen from './components/LoadingScreen'
import ResultsDashboard from './components/ResultsDashboard'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const loadingRef = useRef(null)
  const resultsRef = useRef(null)

  useEffect(() => {
    if (loading) {
      window.setTimeout(() => {
        loadingRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    }
  }, [loading])

  useEffect(() => {
    if (results && !loading) {
      window.setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 150)
    }
  }, [results, loading])

  const handleAudit = async (username, resumeFile, githubToken, liveUrl) => {
    setLoading(true)
    setResults(null)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('username', username)
      if (resumeFile) {
        formData.append('resume_file', resumeFile)
      }
      if (githubToken) {
        formData.append('user_github_token', githubToken)
      }
      if (liveUrl) {
        formData.append('live_url', liveUrl)
      }

      const { data } = await axios.post(`${API_BASE}/audit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResults(data)
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.message ||
        'Something went wrong. Is the backend running?'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#07070f] text-white overflow-x-hidden">
      <Hero />

      <InputPanel onSubmit={handleAudit} loading={loading} />

      <AnimatePresence>
        {error && !loading && (
          <motion.div
            key="error"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="max-w-2xl mx-auto px-6 mt-4 mb-8"
          >
            <div className="glass-card glow-red rounded-2xl p-5 flex items-start gap-3">
              <span className="text-2xl flex-shrink-0">!</span>
              <div>
                <p className="text-red-300 font-semibold text-sm">Analysis Failed</p>
                <p className="text-red-400/80 text-sm mt-1">{error}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div ref={loadingRef}>
        <AnimatePresence>
          {loading && <LoadingScreen key="loading" />}
        </AnimatePresence>
      </div>

      <div ref={resultsRef}>
        <AnimatePresence>
          {results && !loading && (
            <ResultsDashboard key="results" data={results} />
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
