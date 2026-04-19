"""
resume_extract.py
-----------------
Helpers for extracting resume text and GitHub identity from uploaded PDFs.
Supports both visible text parsing and embedded PDF hyperlink annotations.
"""

import io
import re
from typing import Optional
from urllib.parse import urlparse

from pypdf import PdfReader

GITHUB_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)(?:[/\s]|$)",
    re.IGNORECASE,
)

GITHUB_HANDLE_PATTERN = re.compile(
    r"(?:github|git hub)\s*[:\-]?\s*@?([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)",
    re.IGNORECASE,
)


def _normalize_github_username(candidate: str) -> Optional[str]:
    username = (candidate or "").strip().strip("/")
    if not username:
        return None

    if len(username) > 39:
        return None

    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        return None

    return username


def _parse_github_username_from_url(url: str) -> Optional[str]:
    if not url:
        return None

    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    if host not in {"github.com", "www.github.com"}:
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None

    # Accept both direct profile links and repo links, but prefer the owner handle.
    return _normalize_github_username(parts[0])


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)
    return "\n".join(pages).strip()


def extract_links_from_pdf_bytes(pdf_bytes: bytes) -> list[str]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    links: list[str] = []

    for page in reader.pages:
        annotations = page.get("/Annots") or []
        for annotation in annotations:
            try:
                obj = annotation.get_object()
                action = obj.get("/A")
                uri = action.get("/URI") if action else None
                if isinstance(uri, str) and uri.strip():
                    links.append(uri.strip())
            except Exception:
                continue

    return links


def extract_github_identity(resume_text: str, pdf_links: Optional[list[str]] = None) -> tuple[Optional[str], Optional[str]]:
    pdf_links = pdf_links or []

    github_links = [link for link in pdf_links if _parse_github_username_from_url(link)]

    # Prefer pure profile links before repo links when both are present.
    github_links.sort(key=lambda link: (urlparse(link).path.count("/"), len(link)))

    for link in github_links:
        username = _parse_github_username_from_url(link)
        if username:
            return username, f"https://github.com/{username}"

    url_match = GITHUB_URL_PATTERN.search(resume_text)
    if url_match:
        username = _normalize_github_username(url_match.group(1))
        if username:
            return username, f"https://github.com/{username}"

    handle_match = GITHUB_HANDLE_PATTERN.search(resume_text)
    if handle_match:
        username = _normalize_github_username(handle_match.group(1))
        if username:
            return username, f"https://github.com/{username}"

    return None, None
