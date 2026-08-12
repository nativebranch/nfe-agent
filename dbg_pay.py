"""Reproduce the payment-request turn via run_async to see the failure."""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from nfe_agent.agent import build_agent

async def main():
    agent = build_agent()
    svc = InMemorySessionService()
    await svc.create_session(app_name="dbg", user_id="u1", session_id="s1")
    runner = Runner(agent=agent, app_name="dbg", session_service=svc)

    msg = "Gere um pedido de pagamento de 3000 reais em USDC"
    print("USER:", msg)
    try:
        async for event in runner.run_async(
            user_id="u1", session_id="s1",
            new_message=Content(role="user", parts=[Part(text=msg)])):
            if event.content and event.content.parts:
                for p in event.content.parts:
                    if p.text:
                        print("AGENT:", p.text[:800])
            if event.is_final_response():
                break
    except Exception as e:
        import traceback
        print("ERROR:", type(e).__name__, str(e)[:300])
        traceback.print_exc(limit=6)

asyncio.run(main())
