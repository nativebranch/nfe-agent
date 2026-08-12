"""List all Gemini models available to this key, grouped by tier."""
import os
from google import genai

def load_env(path):
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env(os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
names = sorted(m.name for m in client.models.list())
for tier in ("gemini-3", "gemini-2.5", "gemini-2.0", "gemini-flash", "gemini-pro"):
    hits = [n for n in names if tier in n and "tts" not in n and "image" not in n and "embedding" not in n and "audio" not in n and "imagen" not in n and "veo" not in n]
    if hits:
        print(f"== {tier} ==")
        for h in hits[:12]:
            print("  ", h)
