"""Smoke test: run one agent turn against the DANFE fixture and print the transcript."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from nfe_agent.agent import build_agent


async def main():
    agent = build_agent()
    app = "smoke"
    svc = InMemorySessionService()
    await svc.create_session(app_name=app, user_id="u1", session_id="s1")
    runner = Runner(agent=agent, app_name=app, session_service=svc)

    fixture = os.path.abspath("tests/fixtures/danfe_fixture.png")
    msg = (f"Extraia a nota fiscal em {fixture}, lance no ledger e me diga o total em reais "
           "e o hash da entrada.")
    print("USER:", msg)
    async for event in runner.run_async(
        user_id="u1", session_id="s1",
        new_message=Content(role="user", parts=[Part(text=msg)])):
        if event.content and event.content.parts:
            for p in event.content.parts:
                if p.text:
                    print("AGENT:", p.text[:900])


asyncio.run(main())
