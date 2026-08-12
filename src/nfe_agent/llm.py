"""Shared LLM client + config (loads .env at project root)."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_client():
    load_env()
    from google import genai
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def default_model() -> str:
    load_env()
    return os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def fallback_model() -> str:
    """Used when the primary model 503s (free-tier spikes)."""
    return os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash")


def generate_with_fallback(contents, config=None, retries: int = 3):
    """Call generate_content with retry + fallback on 503 (high demand)."""
    import time
    from google.genai import errors
    client = get_client()
    last_err = None
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model=default_model(), contents=contents, config=config)
        except errors.ServerError as e:
            last_err = e
            if e.code != 503:
                raise
            time.sleep(2 * (attempt + 1))
    # primary exhausted -> fallback model
    try:
        return client.models.generate_content(
            model=fallback_model(), contents=contents, config=config)
    except Exception as e:
        raise last_err or e
