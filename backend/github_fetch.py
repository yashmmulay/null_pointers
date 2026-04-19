"""
github_fetch.py
───────────────
Fetches top repos (non-fork, sorted by stars) and preferred code files
from the GitHub REST API without cloning anything.
"""

import asyncio
import base64
import os
from typing import Optional

import httpx

GITHUB_API = "https://api.github.com"

# Preferred file extensions in priority order
PREFERRED_EXTENSIONS = [".py", ".js", ".ts", ".java", ".go", ".cpp", ".rb", ".rs", ".kt"]

# Paths to skip entirely
SKIP_PATHS = {
    "node_modules", "venv", ".venv", "__pycache__", "vendor",
    "dist", "build", ".min.", "migrations", "test", "spec",
    "fixture", "mock", "generated", "proto",
}


def _make_headers(token: Optional[str]) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def _should_skip(path: str) -> bool:
    lower = path.lower()
    return any(skip in lower for skip in SKIP_PATHS)


def _ext_priority(path: str) -> int:
    for i, ext in enumerate(PREFERRED_EXTENSIONS):
        if path.endswith(ext):
            return i
    return len(PREFERRED_EXTENSIONS)


async def fetch_top_repos(username: str, token: Optional[str] = None) -> list[dict]:
    """
    Returns the top 5 non-fork repos sorted by star count.
    Raises ValueError on bad username or API errors.
    """
    headers = _make_headers(token)

    async with httpx.AsyncClient(timeout=20) as client:
        # If token provided, we use the authenticated user endpoint to grab private repos too
        if token:
            resp = await client.get(
                f"{GITHUB_API}/user/repos",
                headers=headers,
                params={"affiliation": "owner", "per_page": 100, "sort": "updated"},
            )
            if resp.status_code == 200:
                # Filter because /user/repos returns the authenticated user's repos,
                # we must ensure it matches the requested username
                all_repos = [r for r in resp.json() if r.get("owner", {}).get("login", "").lower() == username.lower()]
                if not all_repos:
                    # Fallback to public endpoint if the token doesn't match the requested username
                    resp = await client.get(
                        f"{GITHUB_API}/users/{username}/repos",
                        headers=headers,
                        params={"type": "owner", "per_page": 100, "sort": "updated"},
                    )
        else:
            resp = await client.get(
                f"{GITHUB_API}/users/{username}/repos",
                headers=headers,
                params={"type": "owner", "per_page": 100, "sort": "updated"},
            )

    if resp.status_code == 404:
        raise ValueError(f"GitHub user '{username}' not found.")
    if resp.status_code == 403:
        raise ValueError(
            "GitHub rate limit exceeded. Add a GITHUB_TOKEN in your .env file or input field."
        )
    if resp.status_code != 200:
        raise ValueError(f"GitHub API error {resp.status_code}: {resp.text[:200]}")

    repos = all_repos if 'all_repos' in locals() and all_repos else resp.json()
    own_repos = [r for r in repos if not r.get("fork", False)]
    own_repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return own_repos[:4]


async def fetch_repo_files(
    username: str, repo_name: str, token: Optional[str] = None
) -> list[dict]:
    """
    Returns the top 3 code files from the repo (content limited to 300 lines).
    """
    headers = _make_headers(token)

    async with httpx.AsyncClient(timeout=30) as client:
        # Try HEAD branch reference first, then fall back to main/master
        tree_data = None
        for ref in ["HEAD", "main", "master"]:
            resp = await client.get(
                f"{GITHUB_API}/repos/{username}/{repo_name}/git/trees/{ref}",
                headers=headers,
                params={"recursive": "1"},
            )
            if resp.status_code == 200:
                tree_data = resp.json()
                break

        if not tree_data:
            return []

        tree = tree_data.get("tree", [])

        # Filter and sort files
        code_files = [
            item
            for item in tree
            if item.get("type") == "blob"
            and any(item["path"].endswith(ext) for ext in PREFERRED_EXTENSIONS)
            and not _should_skip(item["path"])
            and item.get("size", 0) < 60_000  # skip huge files
        ]
        code_files.sort(key=lambda f: _ext_priority(f["path"]))
        top_files = code_files[:5]

        # Fetch contents concurrently (capped for speed)
        sem = asyncio.Semaphore(15)

        async def fetch_one(file_item):
            async with sem:
                content_resp = await client.get(
                    f"{GITHUB_API}/repos/{username}/{repo_name}/contents/{file_item['path']}",
                    headers=headers,
                )
                if content_resp.status_code != 200:
                    return None

                data = content_resp.json()
                try:
                    raw_bytes = base64.b64decode(data.get("content", ""))
                    raw_text = raw_bytes.decode("utf-8", errors="replace")
                    
                    lines = raw_text.splitlines()[:200]
                    content = "\n".join(lines)
                    return {
                        "filename": file_item["path"],
                        "content": content,
                        "line_count": len(raw_text.splitlines()),
                        "extension": os.path.splitext(file_item["path"])[1],
                    }
                except Exception:
                    return None

        # Fetch limited files concurrently
        tasks = [fetch_one(f) for f in top_files]
        results = await asyncio.gather(*tasks)
        fetched = [r for r in results if r is not None]

    return fetched


async def fetch_all_repos_data(username: str, token: Optional[str] = None) -> list[dict]:
    """
    Orchestrates fetching top repos + their code files.
    Returns a list of repo dicts, each containing a 'files' key.
    """
    repos = await fetch_top_repos(username, token)

    result = []
    for repo in repos:
        files = await fetch_repo_files(username, repo["name"], token)
        result.append(
            {
                "name": repo["name"],
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description") or "",
                "language": repo.get("language") or "Unknown",
                "url": repo.get("html_url", ""),
                "homepage": repo.get("homepage", ""),
                "files": files,
            }
        )

    return result
