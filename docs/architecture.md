# NF-e Agent — Architecture

```
                        ┌────────────────────────────────────────────┐
                        │              USER (freelancer)             │
                        │   WhatsApp/Telegram/Web · PT-BR chat       │
                        └───────────────┬────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        GEMINI ADK AGENT (nf_agent)                     │
│  instruction: pt-BR bookkeeping copilot, fail-closed money rules       │
│  model: gemini-3.6-flash (fallback 3.5-flash on 503)                   │
│                                                                         │
│  tools:                                                                 │
│   extract_invoice  → XML (deterministic) | PDF/photo (Gemini vision)   │
│   book_invoice     → ledger, PTAX valuation, dup/total checks          │
│   request_payment  → reference-key payment proposal (capped)           │
│   verify_payment   → on-chain settlement check (fail-closed)           │
│   export_ledger    → accountant CSV                                    │
└──────────┬──────────────┬──────────────┬───────────────┬───────────────┘
           │              │              │               │
           ▼              ▼              ▼               ▼
   ┌────────────┐  ┌─────────────┐  ┌───────────┐  ┌──────────────┐
   │  EXTRACT   │  │   LEDGER    │  │  PAY RAIL │  │    EXPORT    │
   │  NF-e v4.00│  │ append-only │  │ Solana Pay│  │ CSV PT-BR    │
   │  parser +  │  │ hash-chain  │  │ URL + ref │  │ hash-chained │
   │  cDV check │  │ (SHA-256)   │  │ key (uuid5│  │ PTAX values  │
   └────────────┘  └─────────────┘  │ , no memo)│  └──────────────┘
                                    └─────┬─────┘
                                          │
                    ┌─────────────────────┼──────────────────┐
                    ▼                     ▼                  ▼
            ┌──────────────┐      ┌──────────────┐   ┌──────────────┐
            │  BCB PTAX    │      │  SOLANA      │   │  OPERATOR    │
            │  (official   │      │  RPC (read)  │   │  approval    │
            │  FX, free)   │      │  devnet→main │   │  out-of-band │
            └──────────────┘      └──────────────┘   └──────────────┘
```

## Trust boundaries
- **Untrusted**: invoice documents, chat messages, webhook bodies, RPC responses.
- **Trusted**: operator config (caps, payout wallets), compiled rules, hash chain.
- **Custody**: T0 read (extract/book/verify/export) + T1 build (payment PROPOSALS only).
  The agent holds NO signing key. Payouts require human approval out-of-band.

## Fail-closed decisions
1. Access key fails check-digit → refuse (official NF-e algorithm, verified).
2. `total != Σ items` (>R$0.01) → refuse, no partial booking.
3. Duplicate access key → refuse.
4. Payment above operator cap → refuse (cap is compiled, not prompted).
5. Settlement without exact reference key / wrong asset / missing txid → NOT paid.
6. PTAX missing for the settlement date → `pending_valuation`, never invented.
7. Prompt injection (admin override, wallet swap, urgency) → documented refusals
   (tests/transcripts/injection_attempts.md).

## State
- Ledger: in-memory + CSV export (hash-chained). SQLite persistence = build step.
- Sessions: ADK InMemorySessionService (web demo).

## Reuse
- `core/` is chain-agnostic (ledger, rules, PTAX, refkey) — reusable by the
  ETHOnline Continuity entry (EVM rail) and ZeroClaw plugin variants.
