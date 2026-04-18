# ─────────────────────────────────────────────────────────────────────────────
# DevAudit — Developer Career Intelligence System
# DevClash 2026 | Team of 5
# ─────────────────────────────────────────────────────────────────────────────

## What It Does

Enter a GitHub username → get a **brutally honest audit** of their code:

| Output | Source |
|---|---|
| Skill Verdict (Junior/Mid/Senior) | radon + bandit + Groq AI |
| Code Flaws (file-level, traceable) | radon complexity + bandit CVEs |
| Resume Bullet Rewriter | Groq llama3-70b (reads actual code) |
| Project Damage Detector | AI flags repos hurting the profile |
| 90-Day Roadmap | AI generates based on specific weaknesses |

## Tech Stack

- **Backend**: Python + FastAPI
- **GitHub data**: GitHub REST API (PAT auth)
- **Static analysis**: radon, bandit, pylint
- **AI brain**: Groq API — llama3-70b-8192 (free tier)
- **Frontend**: React + Vite

## Project Structure

```
devaudit/
├── backend/
│   ├── main.py           # FastAPI app (Member 4)
│   ├── github_fetch.py   # GitHub pipeline (Member 1)
│   ├── analyzer.py       # radon + bandit (Member 2)
│   ├── ai_review.py      # Groq AI prompts (Member 3)
│   ├── requirements.txt
│   └── .env              # (never commit this)
├── frontend/             # React Vite app (Member 5)
└── README.md
```

## Quick Start (Backend)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env    # fill in your tokens
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

## Quick Start (Frontend)

```bash
cd frontend
npm install
npm run dev
```

UI: http://localhost:5173

## Environment Variables

```ini
GITHUB_TOKEN=ghp_...   # github.com/settings/tokens → repo scope
GROQ_API_KEY=gsk_...   # console.groq.com/keys
```

## API

### `POST /audit`

```json
{
  "username": "torvalds",
  "resume_bullet": "Built REST APIs and deployed to AWS"
}
```

### Response

```json
{
  "skill_verdict": "Senior",
  "code_flaws": [{"repo": "...", "file": "...", "issue": "..."}],
  "resume_rewrite": {"before": "...", "after": "..."},
  "project_damage": [{"repo": "...", "reason": "..."}],
  "roadmap": ["..."]
}
```

### `GET /health`

Returns token configuration status.

### `GET /contract`

Returns the frozen module interface contract for:
- `get_github_data(username)`
- `analyze_code(github_data)`
- `run_ai_review(github_data, analysis, resume_bullet)`

Use this endpoint to keep backend, AI, analyzer, and frontend aligned during parallel work.

## Team Branch Strategy

- `main`: only stable demo-ready code
- `develop`: integration branch
- `feature/github-fetch-member1`: Member 1 owns `github_fetch.py`
- `feature/analyzer-member2`: Member 2 owns `analyzer.py`
- `feature/ai-review-member3`: Member 3 owns `ai_review.py`
- `feature/backend-api-member4`: Member 4 owns `main.py`, `requirements.txt`, `.env.example`, `README.md`
- `feature/frontend-member5`: Member 5 owns `frontend/`

Merge rules:
- Everyone branches from `develop`
- Everyone merges back into `develop`
- Only merge `develop` into `main` after a working end-to-end demo
- Avoid multiple people editing `main.py`, `requirements.txt`, `.env.example`, or `README.md` at the same time

## Exact Build Order

1. Member 4 freezes API contract in `main.py`
2. Member 5 builds frontend against the contract and mock `/audit` output
3. Member 1 implements GitHub fetch in `github_fetch.py`
4. Member 2 implements static analysis in `analyzer.py`
5. Member 3 implements Groq prompts in `ai_review.py`
6. Member 4 integrates all modules and tests `/audit`

## 4:30 PM Demo Checklist

By 4:30 PM, the demo should show:
- GitHub username input working
- Backend `POST /audit` working
- Top 5 public repos fetched
- Static analysis output from radon and bandit
- Skill verdict shown
- Three file-level code flaws shown with file references
- Resume bullet rewrite before/after
- Project damage detector output
- 90-day roadmap output

Out of scope for this hackathon build:
- job market scraping
- percentile ranking
- live URL or Lighthouse auditing
- deep commit history analysis
