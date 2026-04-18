"""
github_fetch.py — STUB
Replace this file with the real implementation once your teammate commits it.
The real function must accept (username: str) and return a dict.
"""

import logging

logger = logging.getLogger(__name__)


def get_github_data(username: str) -> dict:
    """
    STUB: returns minimal placeholder data.
    Real implementation should call the GitHub API and return repo/code data.
    """
    logger.warning(f"[STUB] get_github_data called for '{username}' — returning placeholder data")
    return {
        "username": username,
        "repos": [
            {
                "name": "sample-repo",
                "language": "Python",
                "stars": 0,
                "files": [
                    {"path": "main.py", "content": "print('hello world')"}
                ],
            }
        ],
    }
