def analyze_audit(data):

    issues = []

    # 1. Title Check
    if not data["title"]:
        issues.append({
            "issue": "Missing Title",
            "category": "SEO",
            "severity": "High",
            "suggestion": "Add a relevant title to the webpage."
        })

    # 2. Meta Description Check
    if not data["meta_description"]:
        issues.append({
            "issue": "Missing Meta Description",
            "category": "SEO",
            "severity": "Medium",
            "suggestion": "Add a meaningful meta description."
        })

    # 3. H1 Check
    if data["h1_count"] == 0:
        issues.append({
            "issue": "Missing H1",
            "category": "SEO",
            "severity": "Medium",
            "suggestion": "Add a descriptive main heading."
        })

    elif data["h1_count"] > 1:
        issues.append({
            "issue": "Multiple H1 Tags",
            "category": "SEO",
            "severity": "Low",
            "suggestion": "Review the heading structure for clarity."
        })

    # 4. Image ALT Check
    if data["images_without_alt"] > 0:
        issues.append({
            "issue": "Images Missing ALT Text",
            "category": "Accessibility",
            "severity": "Medium",
            "suggestion": "Add appropriate ALT text to informative images."
        })

    # 5. HTTPS Check
    if not data["https"]:
        issues.append({
            "issue": "HTTPS Not Enabled",
            "category": "Security",
            "severity": "High",
            "suggestion": "Configure HTTPS with a valid TLS certificate."
        })

    # 6. Broken Links Check
    if data["broken_links"] > 0:
        issues.append({
            "issue": "Broken Links Found",
            "category": "Technical SEO",
            "severity": "Medium",
            "suggestion": (
                f"Check and fix the {data['broken_links']} broken link(s)."
            )
        })

    # 7. Mobile Viewport Check
    if not data["mobile_viewport"]:
        issues.append({
            "issue": "Mobile Viewport Missing",
            "category": "Mobile Compatibility",
            "severity": "Medium",
            "suggestion": (
                "Add a responsive viewport meta tag to the webpage."
            )
        })

    return issues


def generate_report(data, issues, category_count, severity_count, website_score):

    report = {
        "url": data["url"],
        "status_code": data["status_code"],
        "total_issues": len(issues),
        "website_score": website_score,
        "category_summary": category_count,
        "severity_summary": severity_count,
        "issues": issues
    }

    return report