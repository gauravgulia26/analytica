import os
from typing import Any

import requests


def get_available_groq_models() -> dict[str, dict[str, Any]]:
    """Return all models available through the Groq API."""
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    models = response.json().get("data", [])

    return {
        model["id"]: {
            "owned_by": model.get("owned_by"),
            "context_window": model.get("context_window"),
            "max_completion_tokens": model.get("max_completion_tokens"),
            "active": model.get("active"),
        }
        for model in models
    }
