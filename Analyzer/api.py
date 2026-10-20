
from ai_recommendations import generate_ai_recommendations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from lighthouse_audit import run_lighthouse
from analyzer import analyze_audit, generate_report
from scaper import scrape_website

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WebsiteRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {"message": "Website Auditor API is running!"}


@app.post("/analyze")
def analyze_website(request: WebsiteRequest):

    url = request.url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # 1. Scrape website
    audit_data = scrape_website(url)

    if audit_data is None:
        return {
            "error": "Website data collect nahi ho paya. URL check karo."
        }

    # 2. Analyze website
    issues = analyze_audit(audit_data)

    # 3. Count categories
    category_count = {}

    for issue in issues:
        category = issue["category"]
        category_count[category] = category_count.get(category, 0) + 1

    # 4. Count severity
    severity_count = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for issue in issues:
        severity = issue["severity"]

        if severity in severity_count:
            severity_count[severity] += 1

    # 5. Calculate website score
    penalty = {
        "High": 15,
        "Medium": 8,
        "Low": 3
    }

    total_penalty = 0

    for issue in issues:
        severity = issue["severity"]

        if severity in penalty:
            total_penalty += penalty[severity]

    website_score = max(0, 100 - total_penalty)

    # 6. Generate report
    report = generate_report(
        audit_data,
        issues,
        category_count,
        severity_count,
        website_score
    )

    # 7. Run Lighthouse audit
    try:
        lighthouse_result = run_lighthouse(url)

    except Exception as e:
        lighthouse_result = {
            "error": f"Lighthouse audit failed: {str(e)}"
        }

    # 8. Add Lighthouse results
    report["lighthouse"] = lighthouse_result

# 9. Generate AI recommendations
    ai_result = generate_ai_recommendations(issues)
    report["ai_recommendations"] = ai_result

# 10. Return final report
    return report
