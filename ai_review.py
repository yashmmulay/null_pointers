"""
ai_review.py — STUB
Replace this file with the real Groq-powered AI review implementation.
The real function must accept (github_data: dict, analysis: dict, resume_bullet: str)
and return a dict matching the AuditResponse structure (or a partial subset of it).
"""

import logging

logger = logging.getLogger(__name__)


def run_ai_review(github_data: dict, analysis: dict, resume_bullet: str = "") -> dict:
    """
    STUB: returns minimal AI-style response.
    Real implementation should call Groq API with repo context and return insights.
    """
    logger.warning("[STUB] run_ai_review called — returning placeholder AI insights")
    username = github_data.get("username", "unknown")
    return {
        "skill_verdict": "Junior",
        "code_flaws": [
            {
                "repo": "sample-repo",
                "file": "main.py",
                "issue": "No error handling present (stub placeholder)",
            }
        ],
        "resume_rewrite": {
            "before": resume_bullet or "No resume bullet provided",
            "after": f"Built and deployed Python applications for {username} demonstrating software engineering fundamentals. (stub placeholder)",
        },
        "project_damage": [
            {
                "repo": "sample-repo",
                "reason": "Missing README and documentation (stub placeholder)",
            }
        ],
        "roadmap": [
            "Learn about error handling and defensive programming",
            "Add CI/CD pipelines to your projects",
            "Contribute to open source to demonstrate collaboration skills",
        ],
    }
