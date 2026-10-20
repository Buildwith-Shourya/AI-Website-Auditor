from analyzer import analyze_audit, generate_report
from scaper import scrape_website

url = input("Enter website URL: ").strip()

if not url.startswith(("http://", "https://")):
    url = "https://" + url

audit_data = scrape_website(url)

if audit_data is None:
    print("Website data collect nahi ho paya. URL check karo.")
    raise SystemExit(1)


# Step 1: Analyze website data
issues = analyze_audit(audit_data)


# Step 2: Count issues category-wise
category_count = {}

for issue in issues:

    category = issue["category"]

    if category in category_count:
        category_count[category] += 1
    else:
        category_count[category] = 1

# Step 3: Count issues by severity

severity_count = {
    "High": 0,
    "Medium": 0,
    "Low": 0
}

for issue in issues:
    severity = issue["severity"]

    if severity in severity_count:
        severity_count[severity] += 1


# Step 4: Display severity summary

print("\n===== SEVERITY ANALYSIS =====")

for severity, count in severity_count.items():
    print(f"{severity}: {count} issue(s)")

# Step 4: Calculate Website Score

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


# Display Website Score

print("\n===== WEBSITE AUDIT SCORE =====")

print("Starting Score: 100")
print("Total Penalty:", total_penalty)
print("Website Score:", website_score, "/100")

# Step 3: Display report
print("\n===== AI WEBSITE AUDITOR =====")

print("Website:", audit_data["url"])

print("\nTotal Issues:", len(issues))

print("\n===== CATEGORY-WISE ANALYSIS =====")

for category, count in category_count.items():
    print(f"{category}: {count} issue(s)")


# Step 4: Display individual issues
print("\n===== DETAILED REPORT =====")

for number, issue in enumerate(issues, start=1):

    print(f"\nIssue {number}: {issue['issue']}")
    print("Category:", issue["category"])
    print("Severity:", issue["severity"])
    print("Suggestion:", issue["suggestion"])



    # Step 5: Generate Structured Report

report = generate_report(
    audit_data,
    issues,
    category_count,
    severity_count,
    website_score
)

print("\n===== STRUCTURED REPORT =====")

from pprint import pprint
pprint(report)