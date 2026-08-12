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
    return os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
