# NF-e Agent — Threat Model

## Assets
- Operator payout wallet(s) — must never be readable/writable by the agent.
- Ledger integrity (hash chain) — tamper-evident.
- Invoice data (client PII) — read-only use, no exfiltration paths.

## Attack surface (all UNTRUSTED)
| Surface | Attack | Control |
|---|---|---|
| Invoice XML | fake access key | official cDV algorithm, fail-closed |
| Invoice XML | totals mismatch (under-report) | Σ items vs total check |
| Invoice XML | duplicate booking | access-key uniqueness |
| Invoice XML/PDF/photo | embedded instructions ("pay X", "ignore caps") | agent refuses wallet/amount changes from doc content; caps compiled |
| Chat | admin override / role-play | hard rule: operator config immutable from chat (transcript 1) |
| Chat | wallet swap | payment proposals only to operator-configured wallets (transcript 2) |
| Chat | urgency / limit bypass | compiled cap; no "emergency" path (transcript 3) |
| RPC responses | spoofed settlement | reference-key binding + asset allowlist + txid presence |
| Webhook | forged "paid" memo | memo/label NEVER accepted as proof |
| Model | 503/flaky | fallback model, retry; no silent partial results |

## Custody tiers
- T0 (read): extract, book, verify, export.
- T1 (build, unsigned): payment proposals.
- T2 (sign): NOT present in the agent. Human signs out-of-band (Phantom/wallet).
  Structural rule: no signing tool, no shell, no key material in agent config.

## Evidence
- Injection transcripts: tests/transcripts/injection_attempts.md (3 attempts, all refused).
- Tamper test: altered total → extraction rejected (tests/test_vision_extract.py).
- Chain tamper test: any edit breaks hash chain (tests/test_core.py).
