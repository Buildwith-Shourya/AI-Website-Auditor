
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "tinyllama"


def generate_ai_recommendations(issues):
    if not issues:
        return {
            "status": "success",
            "model": MODEL_NAME,
            "recommendations": [
                "No issues were detected by the current website checks."
            ]
        }

    prompt = f"""
You are an assistant for an AI Website Auditor.

Explain the website issues listed below and give practical fixes.
Use simple English.
Give at most 3 short recommendations.
Only use the provided issues. Do not invent audit results.
Do not repeat the entire issue list.

Website issues:
{issues}

Return only a numbered list of recommendations.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You provide concise, practical website "
                            "improvement recommendations based only "
                            "on the supplied audit findings."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 180
                }
            },
            timeout=90
        )

        response.raise_for_status()
        data = response.json()

        recommendation_text = data.get("message", {}).get(
            "content", ""
        ).strip()

        if not recommendation_text:
            raise ValueError("TinyLlama returned an empty response.")

        return {
            "status": "success",
            "model": MODEL_NAME,
            "recommendations": recommendation_text
        }

    except Exception as e:
        return {
            "status": "unavailable",
            "model": MODEL_NAME,
            "recommendations": (
                "AI recommendations are temporarily unavailable. "
                "Please ensure Ollama is running and try again."
            ),
            "error": str(e)
        }
