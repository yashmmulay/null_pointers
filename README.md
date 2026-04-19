# Developer Career Intelligence System

> **Hackathon Project** — Analyze a developer's real GitHub code and generate a brutally honest skill audit using static analysis + AI.

---

## Project Structure

```
devaudit/
├── backend/
│   ├── main.py            ← FastAPI app  (POST /audit, GET /health)
│   ├── github_fetch.py    ← GitHub REST API (top repos + code files)
│   ├── analyzer.py        ← radon + bandit + pylint + JS lint
│   ├── ai_review.py       ← Groq LLaMA 3 70B integration
│   ├── requirements.txt
│   ├── .env               ← your keys go here (copy of .env.example)
│   └── .env.example
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── config.js
        └── components/
            ├── Hero.jsx
            ├── InputPanel.jsx
            ├── LoadingScreen.jsx
            ├── ResultsDashboard.jsx
            ├── SkillVerdict.jsx
            ├── IssuesPanel.jsx
            ├── ResumeRewriter.jsx
            ├── DamagingProjects.jsx
            └── Roadmap.jsx
```

---

## ⚡ Quick Setup (5 minutes)

### Step 1 — Get API Keys

| Service | URL | Cost |
|---------|-----|------|
| **Gemini API** (required) | https://aistudio.google.com/api-keys | Free |
| **GitHub Token** (optional) | https://github.com/settings/tokens | Free |

### Step 2 — Configure Backend

Open `backend/.env` and add your keys:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3 — Install & Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend will be live at: http://localhost:8000

### Step 4 — Install & Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be live at: http://localhost:5173

---

## API Reference

### `POST /audit`

**Request:**
```json
{
  "username": "torvalds",
  "resume_bullet": "Built scalable systems in C and Linux kernel..."
}
```

**Response:**
```json
{
  "success": true,
  "username": "torvalds",
  "repos_analyzed": [...],
  "analysis": {
    "skill_verdict": "Senior",
    "issues": [...],
    "resume_rewrite": { "before": "...", "after": "..." },
    "damaging_projects": [...],
    "roadmap": [...]
  }
}
```

### `GET /health`
Returns `{ status: "ok", groq_configured: true, github_token_configured: true }`

---

## How It Works

1. **Fetch** — Top 5 non-fork repos sorted by stars; top 3 code files per repo
2. **Analyze** — radon (complexity + maintainability), bandit (security), pylint (lint)  
3. **AI Review** — All real code + analysis sent to Groq LLaMA 3 70B
4. **Report** — Skill verdict, issues with fixes, resume rewrite, damaging projects, 90-day roadmap

---

## Tech Stack

- **Backend**: FastAPI + Python 3.11+
- **AI**: Groq API (llama3-70b-8192) — free tier
- **Static Analysis**: radon, bandit, pylint
- **Frontend**: React 18 + Vite + Tailwind CSS + Framer Motion
