"""Test payment proposal flow end-to-end (under cap)."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from nfe_agent.agent import build_agent

async def main():
    agent = build_agent()
    svc = InMemorySessionService()
    await svc.create_session(app_name="dbg2", user_id="u1", session_id="s1")
    runner = Runner(agent=agent, app_name="dbg2", session_service=svc)

    fixture = os.path.abspath("tests/fixtures/danfe_fixture.png")
    msgs = [
        f"Extraia a nota fiscal em {fixture} e lance no ledger",
        "Gere um pedido de pagamento de 250 reais em USDC",
    ]
    for msg in msgs:
        print("\nUSER:", msg)
        try:
            async for event in runner.run_async(
                user_id="u1", session_id="s1",
                new_message=Content(role="user", parts=[Part(text=msg)])):
                if event.content and event.content.parts:
                    for p in event.content.parts:
                        if p.text:
                            print("AGENT:", p.text[:600])
                if event.is_final_response():
                    break
        except Exception as e:
            print("ERROR:", type(e).__name__, str(e)[:200])

asyncio.run(main())
