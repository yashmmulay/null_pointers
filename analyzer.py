"""
analyzer.py — STUB
Replace this file with the real radon + bandit analysis implementation.
The real function must accept (github_data: dict) and return a dict.
"""

import logging

logger = logging.getLogger(__name__)


def analyze_code(github_data: dict) -> dict:
    """
    STUB: returns empty analysis.
    Real implementation should run radon (complexity) + bandit (security) and
    return structured findings.
    """
    logger.warning("[STUB] analyze_code called — returning placeholder analysis")
    return {
        "skill_verdict": "Junior",
        "code_flaws": [],
        "project_damage": [],
        "roadmap": ["Add unit tests", "Improve code documentation"],
    }
