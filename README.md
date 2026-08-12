# NF-e Agent (ATA 2026 entry)

Bookkeeping copilot for Brazilian freelancers: NF-e/PDF intake -> PTAX-valued ledger ->
stablecoin payment requests -> on-chain settlement verification -> accountant-ready export.

Built for the All Things Agentic Hackathon (Google/Devpost, deadline 2026-08-31 21:00 GMT-3).

## Status
- Specs: specs.md (OpenSpec-style, includes AI-attribution plan)
- Research done: BCB PTAX API verified live (2026-08-11 USD: 5.0992/5.0998);
  x402 spec now at github.com/x402-foundation/x402; Google ADK docs at google.github.io/adk-docs
- Build: skeleton (this repo), implementation in progress

## AI-assisted development disclosure (per hackathon rules)
- Specs and this README authored with AI assistance (full prompt history in prompts/)
- All code commits during the Submission Period (Aug 3-31) are tracked in git history
- Prompt-injection tests + transcripts in tests/transcripts/

## Layout
```
specs.md          # full build spec
prompts/          # AI prompts used (attribution)
src/nfe_agent/    # ADK agent: core/ (ledger, ptax, refkey, rules, nfe_parse),
                  # extract.py (Gemini vision), agent.py (tools), webapp.py (FastAPI)
web/index.html    # single-page UI (dark, PT-BR): upload NF-e, chat, ledger view
tests/            # host tests + fixtures (NF-e XML, DANFE PNG) + injection transcripts
docs/             # architecture diagram, threat model, demo script
```

## Run (web)
```
.venv/bin/python -m nfe_agent.webapp   # http://127.0.0.1:8090
```

## Status
- Core: ledger hash-chain, PTAX (BCB, live-tested), reference keys, NF-e v4.00 parser
  with official check-digit, fail-closed rules — 10 tests passing
- Vision extraction: gemini-3.6/3.5-flash, validated output, tamper rejection
- Agent: ADK, 5 tools, pt-BR, prompt-injection refusals documented
- Web: upload -> extract -> book -> chat -> ledger export
