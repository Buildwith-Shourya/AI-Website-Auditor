
import json
import os
import subprocess
import tempfile


LIGHTHOUSE_PATH = (
    "/Users/shouryajeetsingh/.npm-global/bin/lighthouse"
)


def run_lighthouse(url: str) -> dict:
    """Run Lighthouse and return the main audit scores."""

    if not os.path.isfile(LIGHTHOUSE_PATH):
        return {
            "error": "Lighthouse executable not found.",
            "path": LIGHTHOUSE_PATH,
        }

    report_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False
        ) as temp_file:
            report_path = temp_file.name

        result = subprocess.run(
            [
                LIGHTHOUSE_PATH,
                url,
                "--output=json",
                f"--output-path={report_path}",
                "--chrome-flags=--headless",
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            return {
                "error": "Lighthouse audit failed.",
                "details": result.stderr[-1500:],
            }

        with open(report_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        categories = report.get("categories", {})

        def get_score(category_name):
            category = categories.get(category_name, {})
            score = category.get("score")

            return (
                round(score * 100)
                if score is not None
                else None
            )

        return {
            "url": report.get("finalDisplayedUrl", url),
            "scores": {
                "performance": get_score("performance"),
                "accessibility": get_score("accessibility"),
                "best_practices": get_score("best-practices"),
                "seo": get_score("seo"),
            },
        }

    except subprocess.TimeoutExpired:
        return {
            "error": "Lighthouse audit timed out after 120 seconds."
        }

    except (OSError, json.JSONDecodeError) as error:
        return {
            "error": f"Could not read Lighthouse report: {error}"
        }

    finally:
        if report_path and os.path.exists(report_path):
            os.remove(report_path)
