"""Verify the Gemini API key works; list available models; pick flash model."""
import os
from dotenv import load_dotenv  # may not be installed; fallback manual parse

def load_env(path):
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env(os.path.join(os.path.dirname(__file__), ".env"))
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
models = [m.name for m in client.models.list()]
flash = [m for m in models if "flash" in m.lower() and "thinking" not in m.lower()]
print("flash candidates:", flash[:10])

model = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
resp = client.models.generate_content(model=model, contents="Reply with exactly: PONG")
print("model used:", model)
print("response:", resp.text[:100])
