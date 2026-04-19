"""
analyzer.py
───────────
Static analysis layer.

Python files  → radon (complexity + maintainability) + bandit + pylint
JS/TS files   → regex-based lint checks
Other files   → basic structural metrics

All subprocess calls use temp files and have timeouts so they never hang.
"""

import json
import os
import re
import subprocess
import tempfile

# ── Try importing radon's Python API ────────────────────────────────────────
try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────────────

def run_analysis_on_repos(repos_data: list) -> list:
    """Run static analysis on all code files across all repos."""
    results = []
    for repo in repos_data:
        for file_data in repo.get("files", []):
            analysis = _analyze_file(
                filename=file_data["filename"],
                content=file_data["content"],
            )
            analysis["repo"] = repo["name"]
            results.append(analysis)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Internal dispatch
# ─────────────────────────────────────────────────────────────────────────────

def _analyze_file(filename: str, content: str) -> dict:
    ext = os.path.splitext(filename)[1].lower()
    result: dict = {
        "filename": filename,
        "extension": ext,
        "line_count": len(content.splitlines()),
        "complexity": [],
        "maintainability": None,
        "security_issues": [],
        "lint_issues": [],
        "summary": {},
    }

    if ext == ".py":
        return _analyze_python(filename, content, result)
    elif ext in (".js", ".ts", ".jsx", ".tsx"):
        return _analyze_js(filename, content, result)
    else:
        return _analyze_generic(filename, content, result)


# ─────────────────────────────────────────────────────────────────────────────
# Python analysis
# ─────────────────────────────────────────────────────────────────────────────

def _analyze_python(filename: str, content: str, result: dict) -> dict:
    # ── Radon: cyclomatic complexity ────────────────────────────────────────
    if RADON_AVAILABLE:
        try:
            blocks = cc_visit(content)
            result["complexity"] = [
                {
                    "name": b.name,
                    "complexity": b.complexity,
                    "rank": b.letter,
                    "lineno": b.lineno,
                }
                for b in blocks
            ]
            if blocks:
                avg = sum(b.complexity for b in blocks) / len(blocks)
                result["summary"]["avg_complexity"] = round(avg, 2)
                result["summary"]["max_complexity"] = max(b.complexity for b in blocks)
        except Exception as exc:
            result["summary"]["complexity_error"] = str(exc)

        # ── Radon: maintainability index ────────────────────────────────────
        try:
            mi = mi_visit(content, multi=True)
            result["maintainability"] = round(mi, 2)
        except Exception as exc:
            result["summary"]["mi_error"] = str(exc)

    # ── Write temp file for subprocess tools ────────────────────────────────
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(content)
        temp_path = fh.name

    try:
        # ── Bandit: security scan ───────────────────────────────────────────
        try:
            proc = subprocess.run(
                ["bandit", "-f", "json", "-q", temp_path],
                capture_output=True,
                text=True,
                timeout=30,
            )
            stdout = proc.stdout.strip()
            if stdout:
                bandit_data = json.loads(stdout)
                result["security_issues"] = [
                    {
                        "severity": iss.get("issue_severity", "LOW"),
                        "confidence": iss.get("issue_confidence", "LOW"),
                        "text": iss.get("issue_text", ""),
                        "line": iss.get("line_number", 0),
                        "test_id": iss.get("test_id", ""),
                    }
                    for iss in bandit_data.get("results", [])[:5]
                ]
                result["summary"]["security_issue_count"] = len(result["security_issues"])
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

        # ── Pylint ──────────────────────────────────────────────────────────
        try:
            proc = subprocess.run(
                [
                    "pylint",
                    "--output-format=json",
                    "--disable=C0114,C0115,C0116,C0301,W0611,R0903",
                    "--max-line-length=120",
                    temp_path,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            stdout = proc.stdout.strip()
            # pylint may write non-JSON lines before the array
            json_start = stdout.find("[")
            if json_start != -1:
                pylint_data = json.loads(stdout[json_start:])
                result["lint_issues"] = [
                    {
                        "type": iss.get("type", ""),
                        "symbol": iss.get("symbol", ""),
                        "line": iss.get("line", 0),
                        "message": iss.get("message", ""),
                    }
                    for iss in pylint_data
                    if iss.get("type") in ("error", "warning", "refactor")
                ][:8]
                result["summary"]["lint_issue_count"] = len(result["lint_issues"])
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass

    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass

    return result


# ─────────────────────────────────────────────────────────────────────────────
# JS / TS basic analysis (regex-based — no subprocess needed)
# ─────────────────────────────────────────────────────────────────────────────

_JS_PATTERNS = [
    (r"console\.log\(", "console.log() left in code", "warning"),
    (r"\beval\s*\(", "eval() is dangerous — code injection risk", "error"),
    (r"\bvar\s+", "Use const/let instead of var", "warning"),
    (r"[^=!]==[^=]", "Use === instead of == (strict equality)", "warning"),
    (r"document\.write\(", "document.write() is dangerous", "error"),
    (r"innerHTML\s*=", "innerHTML assignment — potential XSS", "warning"),
    (r"new\s+Function\s*\(", "new Function() is risky — like eval()", "error"),
    (r"setTimeout\s*\(\s*['\"]", "setTimeout with string arg — eval risk", "warning"),
]


def _analyze_js(filename: str, content: str, result: dict) -> dict:
    lines = content.splitlines()
    issues = []
    for lineno, line in enumerate(lines, 1):
        for pattern, message, severity in _JS_PATTERNS:
            if re.search(pattern, line):
                issues.append(
                    {
                        "type": severity,
                        "symbol": "js-lint",
                        "line": lineno,
                        "message": message,
                    }
                )
    result["lint_issues"] = issues[:8]
    result["summary"]["lint_issue_count"] = len(result["lint_issues"])

    # Rough complexity: count functions
    func_count = len(re.findall(r"\bfunction\b|=>\s*\{|\basync\s+function\b", content))
    result["summary"]["function_count"] = func_count
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Generic (Java, Go, Rust, etc.)
# ─────────────────────────────────────────────────────────────────────────────

def _analyze_generic(filename: str, content: str, result: dict) -> dict:
    lines = content.splitlines()
    func_keywords = ("def ", "function ", "func ", "void ", "public ", "private ", "protected ")
    result["summary"]["function_count"] = sum(
        1 for line in lines if any(kw in line for kw in func_keywords)
    )
    return result
