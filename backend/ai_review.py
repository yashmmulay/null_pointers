"""
ai_review.py
------------
Deterministic audit engine for developer reports.
The core scores are derived from code analysis and resume heuristics so the
same input produces the same ATS score, market standing, and UI/UX section.
"""

import math
import os
import re
from typing import Optional


CACHE_FILE = "audit_cache.json"
CACHE_VERSION = "v3-deterministic"


def _load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        try:
            import json

            with open(CACHE_FILE, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            return {}
    return {}


def _save_cache(cache_data: dict):
    try:
        import json

        with open(CACHE_FILE, "w", encoding="utf-8") as handle:
            json.dump(cache_data, handle)
    except Exception:
        pass


def _make_signature(username: str, repos_data: list, analysis_results: list, resume_text: str, ui_audit_data: dict) -> str:
    import hashlib

    chunks = [CACHE_VERSION, username.strip().lower(), str(resume_text or "").strip(), str(ui_audit_data.get("url_audited", ""))]
    for repo in repos_data:
        chunks.append(
            f"{repo.get('name','')}|{repo.get('stars',0)}|{repo.get('language','')}|{repo.get('homepage','')}"
        )
        for file_data in repo.get("files", []):
            chunks.append(f"{repo.get('name','')}/{file_data.get('filename','')}|{file_data.get('line_count',0)}")
    for result in analysis_results:
        chunks.append(
            f"{result.get('repo','')}/{result.get('filename','')}|"
            f"{result.get('maintainability')}|"
            f"{result.get('summary',{}).get('avg_complexity')}|"
            f"{len(result.get('security_issues', []))}|{len(result.get('lint_issues', []))}"
        )
    return hashlib.md5("||".join(chunks).encode("utf-8")).hexdigest()


def _tech_keywords() -> dict:
    return {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "React",
        ".ts": "TypeScript",
        ".tsx": "React",
        ".java": "Java",
        ".go": "Go",
        ".rs": "Rust",
        ".cpp": "C++",
        ".kt": "Kotlin",
        ".html": "HTML",
        ".css": "CSS",
    }


def _resume_source(resume_text: Optional[str]) -> str:
    candidate = " ".join((resume_text or "").split())
    if not candidate:
        return ""
    return candidate[:320]


def _collect_repo_techs(repos_data: list, resume_text: str) -> list[str]:
    techs = set()
    ext_map = _tech_keywords()

    for repo in repos_data:
        language = str(repo.get("language") or "").strip()
        if language:
            techs.add(language)
        for file_data in repo.get("files", []):
            ext = file_data.get("extension") or os.path.splitext(file_data.get("filename", ""))[1]
            if ext in ext_map:
                techs.add(ext_map[ext])

            content = (file_data.get("content") or "").lower()
            if "fastapi" in content:
                techs.add("FastAPI")
            if "flask" in content:
                techs.add("Flask")
            if "react" in content:
                techs.add("React")
            if "next" in content:
                techs.add("Next.js")
            if "mongodb" in content or "mongoose" in content:
                techs.add("MongoDB")
            if "sql" in content or "select " in content:
                techs.add("SQL")
            if "node" in content or "express" in content:
                techs.add("Node.js")

    resume_lower = (resume_text or "").lower()
    named_keywords = {
        "fastapi": "FastAPI",
        "flask": "Flask",
        "react": "React",
        "express": "Express",
        "mongodb": "MongoDB",
        "firebase": "Firebase",
        "gemini": "Gemini",
        "sql": "SQL",
    }
    for raw, proper in named_keywords.items():
        if raw in resume_lower:
            techs.add(proper)
    if "node.js" in resume_lower or "nodejs" in resume_lower:
        techs.add("Node.js")

    return sorted(techs)


def _frontend_files(repos_data: list) -> list[str]:
    output = []
    for repo in repos_data:
        for file_data in repo.get("files", []):
            path = f"{repo['name']}/{file_data['filename']}"
            lower = path.lower()
            if lower.endswith((".js", ".jsx", ".ts", ".tsx", ".css", ".html")):
                output.append(path)
    return output


def _analysis_summary(analysis_results: list) -> dict:
    maintainability_values = [r["maintainability"] for r in analysis_results if r.get("maintainability") is not None]
    complexities = [
        r.get("summary", {}).get("avg_complexity")
        for r in analysis_results
        if r.get("summary", {}).get("avg_complexity") is not None
    ]

    total_security = sum(len(r.get("security_issues", [])) for r in analysis_results)
    total_lint = sum(len(r.get("lint_issues", [])) for r in analysis_results)
    high_complexity_files = sum(
        1 for r in analysis_results
        if (r.get("summary", {}).get("max_complexity") or 0) > 10
    )

    return {
        "avg_maintainability": round(sum(maintainability_values) / len(maintainability_values), 2) if maintainability_values else 55.0,
        "avg_complexity": round(sum(complexities) / len(complexities), 2) if complexities else 6.0,
        "total_security": total_security,
        "total_lint": total_lint,
        "high_complexity_files": high_complexity_files,
        "files_analyzed": len(analysis_results),
    }


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _quality_score(summary: dict, repos_data: list) -> int:
    repo_count = len(repos_data)
    stars = sum(int(repo.get("stars", 0) or 0) for repo in repos_data)
    maintainability_score = summary["avg_maintainability"]
    complexity_score = _clamp(100 - ((summary["avg_complexity"] - 2) * 8), 25, 100)
    security_score = _clamp(100 - summary["total_security"] * 12, 10, 100)
    lint_score = _clamp(100 - summary["total_lint"] * 3, 25, 100)
    portfolio_score = _clamp(45 + repo_count * 8 + min(math.log10(stars + 1) * 10, 18), 45, 85)

    score = (
        maintainability_score * 0.34
        + complexity_score * 0.24
        + security_score * 0.18
        + lint_score * 0.12
        + portfolio_score * 0.12
    )
    return int(round(_clamp(score, 15, 95)))


def _skill_verdict(score: int) -> str:
    if score >= 78:
        return "Senior"
    if score >= 55:
        return "Mid"
    return "Junior"


def _percentile_ranking(score: int) -> str:
    top_percent = int(round(_clamp(90 - (score * 0.8), 10, 85)))
    return f"Top {top_percent}% of audited developers"


def _salary_gap(score: int, summary: dict, techs: list[str]) -> str:
    weaknesses = []
    if summary["avg_maintainability"] < 65:
        weaknesses.append("cleaner architecture and maintainability")
    if summary["avg_complexity"] > 8:
        weaknesses.append("simpler control flow in complex modules")
    if summary["total_security"] > 0:
        weaknesses.append("stronger secure coding discipline")
    if summary["total_lint"] > 8:
        weaknesses.append("more consistent code quality hygiene")
    if len(techs) < 4:
        weaknesses.append("broader proof of stack depth")

    if not weaknesses:
        weaknesses.append("clearer evidence of production-scale impact")

    if score >= 78:
        prefix = "To move into a stronger senior bracket, focus on "
    elif score >= 55:
        prefix = "To move into the next mid-to-senior bracket, focus on "
    else:
        prefix = "To move beyond entry-level salary bands, focus on "

    return prefix + ", ".join(weaknesses[:3]) + "."


def _top_issues(analysis_results: list) -> list[dict]:
    issues = []
    for result in analysis_results:
        file_path = f"{result['repo']}/{result['filename']}"
        for security in result.get("security_issues", [])[:2]:
            issues.append(
                {
                    "file": file_path,
                    "problem": f"Security risk ({security.get('severity', 'LOW')}) near line {security.get('line', 0)}: {security.get('text', 'Issue detected.')}",
                    "fix": "Remove the unsafe pattern, validate inputs, and add a regression test for the affected path.",
                    "priority": 100 if security.get("severity") == "HIGH" else 90,
                }
            )

        max_complexity = result.get("summary", {}).get("max_complexity") or 0
        if max_complexity > 10:
            issues.append(
                {
                    "file": file_path,
                    "problem": f"High cyclomatic complexity detected (max {max_complexity}), which makes the module harder to test and maintain.",
                    "fix": "Split the function into smaller units, isolate branching logic, and add focused tests around each decision path.",
                    "priority": 80,
                }
            )

        for lint_issue in result.get("lint_issues", [])[:1]:
            issues.append(
                {
                    "file": file_path,
                    "problem": f"Code quality warning near line {lint_issue.get('line', 0)}: {lint_issue.get('message', 'Lint issue detected.')}",
                    "fix": "Refactor the local code smell and enforce the rule in future changes with linting in CI.",
                    "priority": 60,
                }
            )

    issues.sort(key=lambda item: item["priority"], reverse=True)

    deduped = []
    seen = set()
    for issue in issues:
        key = (issue["file"], issue["problem"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(
            {
                "file": issue["file"],
                "problem": issue["problem"],
                "fix": issue["fix"],
            }
        )
        if len(deduped) >= 6:
            break
    return deduped


def _job_matches(techs: list[str], verdict: str) -> list[dict]:
    tech_set = set(techs)
    matches = []

    if {"React", "JavaScript", "TypeScript"} & tech_set:
        matches.append({"role": "Frontend Engineer", "companies": "SaaS startups, product teams, and web-platform companies", "type": "Remote"})
    if {"Python", "FastAPI", "Flask", "Node.js", "SQL"} & tech_set:
        matches.append({"role": "Backend Engineer", "companies": "API-first startups, internal platform teams, and B2B product companies", "type": "Remote"})
    if {"React", "Python", "Node.js", "FastAPI"} & tech_set:
        matches.append({"role": "Full Stack Engineer", "companies": "Startup engineering teams and growth-stage product companies", "type": "Hybrid"})
    if "Gemini" in tech_set and "Python" in tech_set:
        matches.append({"role": "Applied AI Engineer", "companies": "AI tooling startups, automation companies, and ML product teams", "type": "Remote"})

    if not matches:
        default_role = "Software Engineer" if verdict != "Junior" else "Junior Software Engineer"
        matches.append({"role": default_role, "companies": "Engineering-led startups and software services teams", "type": "Remote"})

    return matches[:4]


def _damaging_projects(repos_data: list, analysis_results: list) -> list[dict]:
    repo_stats = {}
    for result in analysis_results:
        repo = result["repo"]
        stat = repo_stats.setdefault(repo, {"security": 0, "lint": 0, "maintainability": []})
        stat["security"] += len(result.get("security_issues", []))
        stat["lint"] += len(result.get("lint_issues", []))
        if result.get("maintainability") is not None:
            stat["maintainability"].append(result["maintainability"])

    findings = []
    for repo in repos_data:
        stat = repo_stats.get(repo["name"], {})
        avg_mi = (
            sum(stat.get("maintainability", [])) / len(stat.get("maintainability", []))
            if stat.get("maintainability")
            else 60
        )
        severity = stat.get("security", 0) * 8 + stat.get("lint", 0) * 2 + max(0, 55 - avg_mi)
        if severity >= 18:
            reason = []
            if stat.get("security", 0) > 0:
                reason.append("it contains security warnings")
            if avg_mi < 55:
                reason.append("its maintainability is weak")
            if stat.get("lint", 0) > 4:
                reason.append("it has several code-quality warnings")
            findings.append({"repo": repo["name"], "reason": "This project hurts the portfolio because " + " and ".join(reason) + "."})

    return findings[:3]


def _roadmap(summary: dict, techs: list[str]) -> list[dict]:
    items = [
        {"phase": "Days 1-20", "week": "Phase 1: Stabilize", "focus": "Fix security findings and highest-complexity files."},
        {"phase": "Days 21-45", "week": "Phase 2: Clean Up", "focus": "Raise maintainability with refactors and lint discipline."},
        {"phase": "Days 46-70", "week": "Phase 3: Ship Better", "focus": "Add measurable impact, tests, and stronger production polish."},
        {"phase": "Days 71-90", "week": "Phase 4: Positioning", "focus": "Package your best stack into a sharper portfolio narrative."},
    ]

    if "React" in techs and "FastAPI" in techs:
        items[2]["focus"] = "Ship one polished full-stack project with metrics and deployment quality."
    elif "Python" in techs:
        items[2]["focus"] = "Publish a cleaner backend or AI project with tests and monitoring."

    if summary["total_security"] == 0 and summary["avg_complexity"] <= 8:
        items[0]["focus"] = "Strengthen test coverage and production-readiness instead of firefighting."

    return items


def _resume_metrics(resume_text: str, techs: list[str]) -> dict:
    text = resume_text or ""
    lowered = text.lower()
    score = 35
    add = []
    remove = []
    change = []

    section_hits = sum(
        1 for token in ["experience", "project", "projects", "skills", "education", "intern", "summary"]
        if token in lowered
    )
    if section_hits >= 4:
        score += 15
    else:
        add.append("Add clearer ATS section headers like Experience, Projects, Skills, and Education.")

    quantified_hits = len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    if quantified_hits >= 5:
        score += 15
    else:
        add.append("Add measurable outcomes with numbers, percentages, latency, users, or throughput.")

    if "github.com" in lowered:
        score += 8
    else:
        add.append("Add your GitHub profile link so recruiters can verify project depth.")

    if "linkedin.com" in lowered:
        score += 5
    else:
        add.append("Add your LinkedIn profile link for recruiter screening completeness.")

    tech_overlap = sum(1 for tech in techs if tech.lower() in lowered)
    if tech_overlap >= 4:
        score += 12
    else:
        add.append("Mirror the strongest technologies from your projects using exact keywords from your stack.")

    if 700 <= len(text) <= 4500:
        score += 10
    else:
        change.append("Adjust resume density so the content is concise but still complete for ATS parsing.")

    weird_symbols = len(re.findall(r"[^\x00-\x7F]", text))
    if weird_symbols > 8:
        remove.append("Remove decorative symbols or copied PDF glyphs that can confuse ATS parsers.")
        score -= 8

    merged_words = len(re.findall(r"[a-z][A-Z]", text))
    if merged_words > 10:
        change.append("Fix merged words and spacing issues caused by PDF export so the resume reads cleanly.")
        score -= 7

    if "responsible for" in lowered or "worked on" in lowered:
        change.append("Replace generic responsibility statements with action plus impact statements.")

    if not remove:
        remove.append("Remove vague filler like hardworking or passionate unless backed by proof.")
    if not change:
        change.append("Turn project descriptions into outcome-driven bullets with stack, scope, and result.")

    score = int(round(_clamp(score, 25, 98)))
    return {
        "score": score,
        "what_to_add": add[:4],
        "what_to_remove": remove[:4],
        "what_to_change": change[:4],
    }


def _resume_rewrite(resume_text: str, techs: list[str], repos_data: list) -> Optional[dict]:
    source = _resume_source(resume_text)
    if not source:
        return None

    top_repos = ", ".join(repo["name"] for repo in repos_data[:2]) or "production-style projects"
    top_techs = ", ".join(techs[:4]) or "modern software stacks"
    rewrite = (
        f"Built and improved {top_repos} using {top_techs}, with visible hands-on work across implementation, "
        "debugging, and code-quality improvement, and should present that work with clearer measurable impact."
    )
    return {"before": source, "after": rewrite}


def _ui_feedback_from_scores(ui_audit_data: dict) -> list[dict]:
    scores = ui_audit_data.get("scores", {})
    metrics = ui_audit_data.get("metrics", {})

    performance = scores.get("performance")
    accessibility = scores.get("accessibility")
    seo = scores.get("seo")

    perf_issue = (
        f"Live performance scored {performance}/100, which suggests the page is doing too much work during initial load."
        if performance is not None
        else "The live app audit could not confirm performance, so load cost still needs review."
    )
    perf_fix = (
        f"Use the live metrics like FCP {metrics.get('first_contentful_paint', 'N/A')} and TBT {metrics.get('total_blocking_time', 'N/A')} to trim blocking scripts, reduce mount-time work, and defer noncritical UI."
    )

    access_issue = (
        f"Accessibility scored {accessibility}/100, which points to labeling, semantics, or keyboard-flow gaps."
        if accessibility is not None
        else "Accessibility needs a code-based review because the live probe did not return a stable score."
    )
    access_fix = "Audit labels, button text, heading order, focus visibility, and keyboard navigation across the main interaction flow."

    seo_issue = (
        f"SEO scored {seo}/100 and CLS is {metrics.get('cumulative_layout_shift', 'N/A')}, so metadata and layout stability need attention."
        if seo is not None
        else "The live app still needs review for metadata quality and layout stability."
    )
    seo_fix = "Add robust metadata, reserve space for dynamic content, and prevent shift-prone elements from moving after first paint."

    return [
        {"metric": "Performance", "issue": perf_issue, "fix": perf_fix},
        {"metric": "Accessibility", "issue": access_issue, "fix": access_fix},
        {"metric": "SEO and Stability", "issue": seo_issue, "fix": seo_fix},
    ]


def _ui_feedback_from_code(repos_data: list, ui_audit_data: dict) -> list[dict]:
    frontend = _frontend_files(repos_data)
    primary = frontend[0] if frontend else "frontend files"
    secondary = frontend[1] if len(frontend) > 1 else primary
    tertiary = frontend[2] if len(frontend) > 2 else primary
    title_prefix = "Live probe was blocked" if ui_audit_data.get("url_audited") else "No live URL was provided"

    return [
        {
            "metric": "Performance",
            "issue": f"{title_prefix}, so performance is estimated from code structure. Review {primary} for heavy initial rendering and unnecessary client work.",
            "fix": f"Split large UI sections, lazy-load secondary panels, and reduce mount-time effects in {primary}.",
        },
        {
            "metric": "Accessibility",
            "issue": f"{secondary} should be checked for semantic markup, visible focus states, and clear input labeling.",
            "fix": f"Use explicit labels, keyboard-safe controls, and semantic headings in {secondary}.",
        },
        {
            "metric": "Interaction",
            "issue": f"{tertiary} should preserve stable loading, success, and error states so the interface does not feel jumpy.",
            "fix": f"Reserve layout space for async content and keep state transitions predictable in {tertiary}.",
        },
    ]


def enrich_ui_audit_data(ui_audit_data: Optional[dict], repos_data: list, analysis_results: list) -> dict:
    ui_audit_data = dict(ui_audit_data or {})
    if not ui_audit_data.get("url_audited"):
        return ui_audit_data

    scores = ui_audit_data.get("scores") or {}
    if any(value is not None for value in scores.values()):
        ui_audit_data["estimated"] = False
        return ui_audit_data

    frontend_count = len(_frontend_files(repos_data))
    total_lint = sum(len(result.get("lint_issues", [])) for result in analysis_results)
    total_security = sum(len(result.get("security_issues", [])) for result in analysis_results)

    performance = int(round(_clamp(72 + frontend_count * 2 - total_lint * 1.5 - total_security * 3, 35, 88)))
    accessibility = int(round(_clamp(70 + min(frontend_count, 4) * 2 - total_lint, 40, 90)))
    best_practices = int(round(_clamp(74 + min(frontend_count, 4) * 2 - total_security * 4, 38, 92)))
    seo = int(round(_clamp(60 + min(frontend_count, 4) * 3, 35, 85)))

    ui_audit_data["scores"] = {
        "performance": performance,
        "accessibility": accessibility,
        "best_practices": best_practices,
        "seo": seo,
    }
    ui_audit_data["metrics"] = ui_audit_data.get("metrics") or {
        "first_contentful_paint": "Estimated from repository structure",
        "largest_contentful_paint": "Estimated from repository structure",
        "speed_index": "Estimated from repository structure",
        "total_blocking_time": "Estimated from repository structure",
        "interactive": "Estimated from repository structure",
        "cumulative_layout_shift": "Estimated from repository structure",
    }
    ui_audit_data["estimated"] = True
    return ui_audit_data


def generate_review(
    username: str,
    repos_data: list,
    analysis_results: list,
    ui_audit_data: Optional[dict] = None,
    resume_text: Optional[str] = "",
) -> dict:
    ui_audit_data = ui_audit_data or {}
    summary = _analysis_summary(analysis_results)
    techs = _collect_repo_techs(repos_data, resume_text or "")
    score = _quality_score(summary, repos_data)
    verdict = _skill_verdict(score)
    signature = _make_signature(username, repos_data, analysis_results, resume_text or "", ui_audit_data)

    cache = _load_cache()
    if signature in cache:
        return cache[signature]

    has_resume = bool((resume_text or "").strip())

    if ui_audit_data.get("url_audited"):
        if any(value is not None for value in (ui_audit_data.get("scores") or {}).values()):
            ui_feedback = _ui_feedback_from_scores(ui_audit_data)
        else:
            ui_feedback = _ui_feedback_from_code(repos_data, ui_audit_data)
    else:
        ui_feedback = []

    result = {
        "skill_verdict": verdict,
        "percentile_ranking": _percentile_ranking(score),
        "salary_bracket_gap": _salary_gap(score, summary, techs),
        "issues": _top_issues(analysis_results),
        "ui_ux_feedback": ui_feedback,
        "job_matches": _job_matches(techs, verdict),
        "damaging_projects": _damaging_projects(repos_data, analysis_results),
        "roadmap": _roadmap(summary, techs),
        "resume_rewrite": _resume_rewrite(resume_text or "", techs, repos_data) if has_resume else None,
        "ats_score": _resume_metrics(resume_text or "", techs) if has_resume else None,
    }

    cache[signature] = result
    _save_cache(cache)
    return result
