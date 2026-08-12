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
src/nfe_agent/    # ADK agent: tools/ (extract, ledger, pay), channels/
tests/            # host tests + fixtures (NF-e XML, DANFE PDF, photo)
docs/             # architecture diagram, threat model, demo script
```

## Run (when implemented)
```
pip install -e ".[dev]"   # google-adk + vision deps
adk run nfe_agent         # or `python -m nfe_agent`
```
