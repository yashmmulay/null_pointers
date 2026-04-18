import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}
if not GITHUB_TOKEN:
    print("Warning: No GitHub token found. Rate limits may apply.")


def get_top_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    params = {"sort": "stars", "per_page": 5}

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Error fetching repos: {response.json()}")

    repos = response.json()

    return [
        {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "default_branch": repo["default_branch"]
        }
        for repo in repos
    ]


def get_repo_files(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return []

    tree = response.json().get("tree", [])

    code_files = [
        file for file in tree
        if file["path"].endswith((".py", ".js", ".ts")) and file["type"] == "blob"
    ]

    return code_files[:2]


def get_file_content(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return None

    content = response.json()

    if content.get("encoding") == "base64":
        import base64
        return base64.b64decode(content["content"]).decode("utf-8", errors="ignore")

    return None


def fetch_github_data(username):
    repos = get_top_repos(username)

    result = []

    for repo in repos:
        owner, repo_name = repo["full_name"].split("/")

        files = get_repo_files(owner, repo_name, repo["default_branch"])

        file_data = []

        for file in files:
            try:
                code = get_file_content(owner, repo_name, file["path"])
            except Exception:
                continue

            if code:
                file_data.append({
                    "filename": file["path"],
                    "code": code[:3000]
                })

        if file_data:
            result.append({
                "repo": repo_name,
                "file_count": len(file_data),
                "files": file_data
            })

    return result 