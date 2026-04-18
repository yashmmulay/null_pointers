"""
Developer Career Intelligence System — FastAPI Backend
=======================================================
POST /audit
Pipeline: github_fetch → analyzer → ai_review → normalized output
"""

import os
import time
import logging
import traceback
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

# ── Logging configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Module imports (guarded — teammates may not have committed yet) ────────────
try:
    from github_fetch import get_github_data
    logger.info("✅ github_fetch module loaded")
except ImportError:
    logger.warning("⚠️  github_fetch not found — using stub")
    def get_github_data(username: str) -> dict:  # type: ignore[misc]
        return {}

try:
    from analyzer import analyze_code
    logger.info("✅ analyzer module loaded")
except ImportError:
    logger.warning("⚠️  analyzer not found — using stub")
    def analyze_code(github_data: dict) -> dict:  # type: ignore[misc]
        return {}

try:
    from ai_review import run_ai_review
    logger.info("✅ ai_review module loaded")
except ImportError:
    logger.warning("⚠️  ai_review not found — using stub")
    def run_ai_review(github_data: dict, analysis: dict, resume_bullet: str = "") -> dict:  # type: ignore[misc]
        return {}

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Developer Career Intelligence API",
    description="Audits a GitHub developer and returns skill verdict, code flaws, resume rewrite, project damage, and roadmap.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic models ───────────────────────────────────────────────────────────
class AuditRequest(BaseModel):
    username: str = Field(..., min_length=1, description="GitHub username to audit")
    resume_bullet: str = Field(default="", description="Optional resume bullet to rewrite")


class CodeFlaw(BaseModel):
    repo: str
    file: str
    issue: str


class ResumRewrite(BaseModel):
    before: str
    after: str


class ProjectDamage(BaseModel):
    repo: str
    reason: str


class AuditResponse(BaseModel):
    skill_verdict: str
    code_flaws: list[CodeFlaw]
    resume_rewrite: ResumRewrite
    project_damage: list[ProjectDamage]
    roadmap: list[str]


MODULE_CONTRACTS = {
    "github_fetch": {
        "function": "get_github_data(username: str) -> dict",
        "required_fields": {
            "username": "str",
            "repos": [
                {
                    "name": "str",
                    "language": "str",
                    "stars": "int",
                    "url": "str",
                    "files": [
                        {
                            "path": "str",
                            "content": "str",
                        }
                    ],
                }
            ],
        },
        "notes": [
            "Return top 5 public repositories only.",
            "Return up to top 3 code files per repository.",
            "Use empty list instead of missing repos/files when nothing is found.",
        ],
    },
    "analyzer": {
        "function": "analyze_code(github_data: dict) -> dict",
        "expected_fields": {
            "skill_verdict": "Junior|Mid|Senior",
            "code_flaws": [
                {
                    "repo": "str",
                    "file": "str",
                    "issue": "str",
                }
            ],
            "project_damage": [
                {
                    "repo": "str",
                    "reason": "str",
                }
            ],
            "roadmap": ["str"],
            "metrics": {
                "repos_analyzed": "int",
                "files_analyzed": "int",
            },
        },
        "notes": [
            "Use radon, bandit, and optional pylint signals.",
            "Keep findings file-level and traceable.",
            "Return JSON-safe data only.",
        ],
    },
    "ai_review": {
        "function": "run_ai_review(github_data: dict, analysis: dict, resume_bullet: str = '') -> dict",
        "expected_fields": {
            "skill_verdict": "Junior|Mid|Senior",
            "code_flaws": [
                {
                    "repo": "str",
                    "file": "str",
                    "issue": "str",
                }
            ],
            "resume_rewrite": {
                "before": "str",
                "after": "str",
            },
            "project_damage": [
                {
                    "repo": "str",
                    "reason": "str",
                }
            ],
            "roadmap": ["str"],
        },
        "notes": [
            "Resume rewrite should be evidence-based from actual repo code.",
            "Damage detector should identify repos that weaken portfolio quality.",
            "Avoid generic advice; use file-level specifics where possible.",
        ],
    },
}


# ── Safe-access helpers ───────────────────────────────────────────────────────
def safe_str(value: Any, default: str = "N/A") -> str:
    """Return a string; fall back to default for None / non-string values."""
    if value is None:
        return default
    try:
        return str(value).strip() or default
    except Exception:
        return default


def safe_list(value: Any, default: list | None = None) -> list:
    """Return a list; coerce single items or fall back to default."""
    if default is None:
        default = []
    if value is None:
        return default
    if isinstance(value, list):
        return value
    if isinstance(value, (str, dict)):
        return [value]
    try:
        return list(value)
    except Exception:
        return default


def safe_dict(value: Any, default: dict | None = None) -> dict:
    """Return a dict; fall back to default for unexpected types."""
    if default is None:
        default = {}
    if isinstance(value, dict):
        return value
    return default


def _elapsed(start: float) -> str:
    return f"{(time.perf_counter() - start) * 1000:.1f}ms"


# ── Normalizers ───────────────────────────────────────────────────────────────
VALID_VERDICTS = {"Junior", "Mid", "Senior"}


def normalize_skill_verdict(raw: Any) -> str:
    """Accept loose strings like 'mid-level', 'senior developer', 'JUNIOR', etc."""
    verdict = safe_str(raw, "Junior").strip()
    for v in VALID_VERDICTS:
        if v.lower() in verdict.lower():
            return v
    return "Junior"


def normalize_code_flaws(raw: Any) -> list[dict]:
    """
    Accepts multiple formats:
      - list of dicts with repo/file/issue keys
      - list of strings
      - single dict
      - None / unexpected type
    """
    items = safe_list(raw)
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append({
                "repo": safe_str(item.get("repo") or item.get("repository") or item.get("name")),
                "file": safe_str(item.get("file") or item.get("path") or item.get("filename")),
                "issue": safe_str(item.get("issue") or item.get("message") or item.get("description") or item.get("error")),
            })
        elif isinstance(item, str) and item.strip():
            result.append({"repo": "unknown", "file": "unknown", "issue": item.strip()})
    return result


def normalize_resume_rewrite(raw: Any, original_bullet: str) -> dict:
    """
    Accepts:
      - dict with 'before'/'after' keys
      - dict with 'original'/'rewritten' keys
      - plain string (treated as 'after')
      - None
    """
    d = safe_dict(raw)
    if d:
        after = safe_str(
            d.get("after") or d.get("rewritten") or d.get("improved") or d.get("new")
        )
        before = safe_str(
            d.get("before") or d.get("original") or d.get("old"),
            default=original_bullet or "No resume bullet provided",
        )
        return {"before": before, "after": after}
    if isinstance(raw, str) and raw.strip():
        return {
            "before": original_bullet or "No resume bullet provided",
            "after": raw.strip(),
        }
    return {
        "before": original_bullet or "No resume bullet provided",
        "after": "Unable to generate resume rewrite at this time.",
    }


def normalize_project_damage(raw: Any) -> list[dict]:
    """
    Accepts:
      - list of dicts with repo/reason keys
      - list of strings
      - single dict
      - None
    """
    items = safe_list(raw)
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append({
                "repo": safe_str(item.get("repo") or item.get("repository") or item.get("project") or item.get("name")),
                "reason": safe_str(item.get("reason") or item.get("issue") or item.get("description") or item.get("problem")),
            })
        elif isinstance(item, str) and item.strip():
            result.append({"repo": "unknown", "reason": item.strip()})
    return result


def normalize_roadmap(raw: Any) -> list[str]:
    """Accept list of strings, a single string, or None."""
    items = safe_list(raw)
    result = []
    for item in items:
        s = safe_str(item)
        if s and s != "N/A":
            result.append(s)
    return result or ["Review code quality fundamentals", "Work on a portfolio project", "Contribute to open source"]


# ── Pipeline merger ───────────────────────────────────────────────────────────
def merge_outputs(
    github_data: dict,
    analysis: dict,
    ai_result: dict,
    resume_bullet: str,
) -> dict:
    """
    Merge analyzer + ai_review into the strict final format.
    Priority: ai_result fields > analyzer fields > defaults.
    """
    logger.info("🔀 Merging pipeline outputs …")

    # ── skill_verdict ─────────────────────────────────────────────────────────
    skill_verdict = normalize_skill_verdict(
        ai_result.get("skill_verdict")
        or ai_result.get("verdict")
        or ai_result.get("level")
        or analysis.get("skill_verdict")
        or analysis.get("level")
    )

    # ── code_flaws ────────────────────────────────────────────────────────────
    ai_flaws = normalize_code_flaws(
        ai_result.get("code_flaws")
        or ai_result.get("flaws")
        or ai_result.get("issues")
    )
    analyzer_flaws = normalize_code_flaws(
        analysis.get("code_flaws")
        or analysis.get("issues")
        or analysis.get("flaws")
    )
    # Combine both sources, de-duplicate by issue text
    seen_issues: set[str] = set()
    code_flaws = []
    for flaw in (ai_flaws + analyzer_flaws):
        key = flaw["issue"].lower()
        if key not in seen_issues and key != "n/a":
            seen_issues.add(key)
            code_flaws.append(flaw)

    # ── resume_rewrite ────────────────────────────────────────────────────────
    resume_rewrite = normalize_resume_rewrite(
        ai_result.get("resume_rewrite")
        or ai_result.get("resume")
        or analysis.get("resume_rewrite"),
        resume_bullet,
    )

    # ── project_damage ────────────────────────────────────────────────────────
    project_damage = normalize_project_damage(
        ai_result.get("project_damage")
        or ai_result.get("damage")
        or ai_result.get("risks")
        or analysis.get("project_damage")
    )

    # ── roadmap ───────────────────────────────────────────────────────────────
    roadmap = normalize_roadmap(
        ai_result.get("roadmap")
        or ai_result.get("recommendations")
        or ai_result.get("suggestions")
        or analysis.get("roadmap")
    )

    return {
        "skill_verdict": skill_verdict,
        "code_flaws": code_flaws,
        "resume_rewrite": resume_rewrite,
        "project_damage": project_damage,
        "roadmap": roadmap,
    }


# ── Endpoint ──────────────────────────────────────────────────────────────────
@app.post("/audit", response_model=AuditResponse, summary="Audit a GitHub developer's profile")
async def audit(request: AuditRequest):
    username = request.username.strip()
    resume_bullet = (request.resume_bullet or "").strip()
    total_start = time.perf_counter()

    logger.info("=" * 60)
    logger.info(f"🚀 /audit  username={username!r}  resume_bullet={'YES' if resume_bullet else 'NO'}")

    github_data: dict = {}
    analysis: dict = {}
    ai_result: dict = {}

    # ── Step 1: GitHub Fetch ──────────────────────────────────────────────────
    step_start = time.perf_counter()
    try:
        raw = get_github_data(username)
        github_data = safe_dict(raw)
        if not github_data:
            logger.warning("⚠️  GitHub fetch returned empty/invalid data — continuing with fallback")
        else:
            logger.info(f"✅ GitHub fetch success  [{_elapsed(step_start)}]  keys={list(github_data.keys())[:5]}")
    except Exception:
        logger.error(f"❌ GitHub fetch FAILED  [{_elapsed(step_start)}]\n{traceback.format_exc()}")

    # ── Step 2: Static Analysis ───────────────────────────────────────────────
    step_start = time.perf_counter()
    try:
        raw = analyze_code(github_data)
        analysis = safe_dict(raw)
        if not analysis:
            logger.warning("⚠️  Analyzer returned empty/invalid data — continuing with fallback")
        else:
            logger.info(f"✅ Analyzer completed  [{_elapsed(step_start)}]  keys={list(analysis.keys())[:5]}")
    except Exception:
        logger.error(f"❌ Analyzer FAILED  [{_elapsed(step_start)}]\n{traceback.format_exc()}")

    # ── Step 3: AI Review ─────────────────────────────────────────────────────
    step_start = time.perf_counter()
    try:
        raw = run_ai_review(github_data, analysis, resume_bullet)
        ai_result = safe_dict(raw)
        if not ai_result:
            logger.warning("⚠️  AI review returned empty/invalid data — continuing with fallback")
        else:
            logger.info(f"✅ AI review completed  [{_elapsed(step_start)}]  keys={list(ai_result.keys())[:5]}")
    except Exception:
        logger.error(f"❌ AI review FAILED  [{_elapsed(step_start)}]\n{traceback.format_exc()}")

    # ── Guard: if all three pipeline steps returned nothing, abort ─────────────
    if not github_data and not analysis and not ai_result:
        logger.critical("💥 All pipeline steps failed — returning error response")
        raise HTTPException(
            status_code=502,
            detail={"error": "All pipeline modules failed. Check server logs for details."},
        )

    # ── Step 4: Merge & normalize ─────────────────────────────────────────────
    try:
        merged = merge_outputs(github_data, analysis, ai_result, resume_bullet)
    except Exception:
        logger.error(f"❌ Merge FAILED\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Output normalization failed. Check server logs."},
        )

    logger.info(f"🏁 /audit complete  total=[{_elapsed(total_start)}]  verdict={merged['skill_verdict']!r}")
    logger.info("=" * 60)
    return merged


# ── Health-check ──────────────────────────────────────────────────────────────
@app.get("/health", summary="Health check")
async def health():
    return {
        "status": "ok",
        "github_token_set": bool(GITHUB_TOKEN),
        "groq_api_key_set": bool(GROQ_API_KEY),
        "frontend_origin": FRONTEND_ORIGIN,
    }


@app.get("/contract", summary="Integration contract for teammate modules")
async def contract():
    return MODULE_CONTRACTS


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
