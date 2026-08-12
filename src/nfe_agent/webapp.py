"""FastAPI web app: upload NF-e -> agent chat -> ledger view."""
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent import build_agent, export_ledger, extract_invoice, book_invoice
from .core.rules import RuleError

app = FastAPI(title="NF-e Agent")
AGENT = build_agent()
WEB_DIR = Path(__file__).resolve().parent.parent.parent / "web"


class ChatBody(BaseModel):
    message: str


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/extract")
async def api_extract(file: UploadFile = File(...)):
    suffix = Path(file.filename or "doc.png").suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    try:
        inv = extract_invoice(path)
        booked = book_invoice(inv)
        return {"invoice": inv, "booked": booked}
    except RuleError as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except Exception as e:
        return JSONResponse({"error": f"extraction failed: {e}"}, status_code=500)


@app.get("/api/ledger")
def api_ledger():
    return {"csv": export_ledger()}


@app.post("/api/chat")
async def api_chat(body: ChatBody):
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import Content, Part

    svc = InMemorySessionService()
    await svc.create_session(app_name="web", user_id="web", session_id="s")
    runner = Runner(agent=AGENT, app_name="web", session_service=svc)
    out = []
    async for event in runner.run_async(
        user_id="web", session_id="s",
        new_message=Content(role="user", parts=[Part(text=body.message)])):
        if event.content and event.content.parts:
            for p in event.content.parts:
                if p.text:
                    out.append(p.text)
    return {"reply": "\n".join(out)}


app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)
