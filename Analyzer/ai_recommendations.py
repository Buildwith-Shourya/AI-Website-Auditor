
import json

MODEL_NAME = "tinyllama"


def generate_ai_recommendations(issues):
    """
    Generate reliable recommendations from confirmed audit findings.
    Never display unverified AI-generated claims.
    """

    if isinstance(issues, str):
        try:
            issues = json.loads(issues)
        except json.JSONDecodeError:
            issues = [{"issue": issues}]

    if isinstance(issues, dict):
        issues = [issues]

    recommendations = []
    seen = set()

    for item in issues or []:
        if not isinstance(item, dict):
            continue

        issue_name = (
            item.get("issue")
            or item.get("name")
            or item.get("title")
        )

        if not issue_name:
            continue

        issue_name = str(issue_name).strip()
        key = issue_name.casefold()

        # Remove duplicate findings.
        if key in seen:
            continue
        seen.add(key)

        suggestion = str(item.get("suggestion", "")).strip()

        if not suggestion:
            suggestion = (
                "Review this confirmed finding and apply "
                "the appropriate fix."
            )

        recommendations.append(
            f"{len(recommendations) + 1}. {issue_name}\n"
            f"   Recommended fix: {suggestion}"
        )

        if len(recommendations) == 3:
            break

    if not recommendations:
        recommendations = [
            "No issues were detected by the current website checks."
        ]

    return {
        "status": "success",
        "model": MODEL_NAME,
        "recommendations": "\n\n".join(recommendations)
    }
