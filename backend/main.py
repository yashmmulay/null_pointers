"""
main.py
--------
FastAPI application with endpoints for:
  1. Resume PDF extraction during audit
  2. GitHub repo + file fetching
  3. Static analysis
  4. Deterministic career review

Run with:
    uvicorn main:app --reload --port 8000
"""

import os
import traceback
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_review import enrich_ui_audit_data, generate_review
from analyzer import run_analysis_on_repos
from github_fetch import fetch_all_repos_data
from resume_extract import extract_text_from_pdf_bytes
from ui_audit import run_ui_audit

load_dotenv()

app = FastAPI(
    title="Developer Career Intelligence System",
    description="Audit real GitHub code with deterministic scoring and static analysis.",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    github_token_configured: bool


@app.get("/", tags=["meta"])
async def root():
    return {
        "message": "DevAudit API is running. Use the frontend at http://localhost:5173",
        "health_check": "/health",
        "audit_endpoint": "/audit",
    }


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health_check():
    return {
        "status": "ok",
        "gemini_configured": False,
        "github_token_configured": bool(os.getenv("GITHUB_TOKEN")),
    }


@app.post("/audit", tags=["audit"])
async def audit(
    username: str = Form(...),
    user_github_token: Optional[str] = Form(""),
    live_url: Optional[str] = Form(""),
    resume_file: Optional[UploadFile] = File(None),
):
    username = username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="GitHub username cannot be empty.")

    resume_text = ""
    if resume_file and resume_file.filename:
        if not resume_file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Resume must be a PDF file.")
        try:
            pdf_bytes = await resume_file.read()
            resume_text = extract_text_from_pdf_bytes(pdf_bytes)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}") from exc

    github_token = user_github_token.strip() if user_github_token else os.getenv("GITHUB_TOKEN")

    try:
        repos_data = await fetch_all_repos_data(username, github_token)
        if not repos_data:
            raise HTTPException(
                status_code=404,
                detail=f"No public repositories found for GitHub user '{username}'.",
            )

        repos_with_files = [repo for repo in repos_data if repo.get("files")]
        if not repos_with_files:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Found {len(repos_data)} repos for '{username}' but none contained "
                    "analyzable code files (.py, .js, .ts, .java, .go, etc.)."
                ),
            )

        analysis_results = run_analysis_on_repos(repos_with_files)

        ui_audit_data = {}
        if live_url and live_url.strip():
            ui_audit_data = await run_ui_audit(live_url.strip())
        else:
            for repo in repos_with_files:
                homepage = repo.get("homepage", "")
                if homepage and homepage.startswith("http"):
                    ui_audit_data = await run_ui_audit(homepage.strip())
                    break

        ui_audit_data = enrich_ui_audit_data(ui_audit_data, repos_with_files, analysis_results)

        analysis = generate_review(
            username=username,
            repos_data=repos_with_files,
            analysis_results=analysis_results,
            ui_audit_data=ui_audit_data,
            resume_text=resume_text,
        )

        return {
            "success": True,
            "username": username,
            "repos_analyzed": [
                {
                    "name": repo["name"],
                    "stars": repo["stars"],
                    "language": repo["language"],
                    "url": repo["url"],
                    "files_analyzed": len(repo["files"]),
                }
                for repo in repos_with_files
            ],
            "live_app_metrics": ui_audit_data,
            "analysis": analysis,
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        print("--- Unhandled error in /audit ---")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(exc)}",
        ) from exc
