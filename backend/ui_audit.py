import httpx


async def run_ui_audit(url: str) -> dict:
    """
    Runs a Lighthouse audit via the Google PageSpeed Insights API and returns
    both headline scores and raw display metrics for the frontend.
    """
    if not url.strip():
        return {}

    if not url.startswith("http"):
        url = "https://" + url

    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = [
        ("url", url),
        ("category", "performance"),
        ("category", "accessibility"),
        ("category", "best-practices"),
        ("category", "seo"),
        ("strategy", "mobile"),
    ]

    async with httpx.AsyncClient(timeout=40) as client:
        try:
            response = await client.get(api_url, params=params)
            if response.status_code != 200:
                return {"url_audited": url, "error": f"Probe blocked: {response.status_code}"}

            data = response.json().get("lighthouseResult", {})
            categories = data.get("categories", {})
            audits = data.get("audits", {})

            def get_score(category_id):
                score = categories.get(category_id, {}).get("score")
                return int(score * 100) if score is not None else None

            def get_metric(audit_id):
                audit = audits.get(audit_id, {})
                return {
                    "display_value": audit.get("displayValue", "N/A"),
                    "numeric_value": audit.get("numericValue"),
                }

            cls_metric = get_metric("cumulative-layout-shift")

            return {
                "url_audited": url,
                "scores": {
                    "performance": get_score("performance"),
                    "accessibility": get_score("accessibility"),
                    "best_practices": get_score("best-practices"),
                    "seo": get_score("seo"),
                },
                "metrics": {
                    "first_contentful_paint": get_metric("first-contentful-paint")["display_value"],
                    "largest_contentful_paint": get_metric("largest-contentful-paint")["display_value"],
                    "speed_index": get_metric("speed-index")["display_value"],
                    "total_blocking_time": get_metric("total-blocking-time")["display_value"],
                    "interactive": get_metric("interactive")["display_value"],
                    "cumulative_layout_shift": cls_metric["display_value"],
                },
                "diagnostics": {
                    "cumulative_layout_shift_value": cls_metric["numeric_value"],
                },
            }
        except Exception as exc:
            return {"url_audited": url, "error": str(exc)}
