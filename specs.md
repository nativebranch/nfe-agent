# ATA Build Specs — "NF-e Agent" (OpenSpec-style, required for AI-attribution)

## spec/project.md
- Name: NF-e Agent (working title; PT-BR first, EN-ready)
- Goal: a Gemini ADK agent that runs the receivables of a one-person Brazilian business:
  invoice intake (NF-e/PDF) -> ledger (PTAX-valued) -> stablecoin payment request ->
  settlement verification -> accountant-ready export. Approval-gated; agent never holds a key.
- Tracks targeted: Individual/Hobbyist ($10k x2) + Best Multimodal UX ($5k x2) + Taskmaster ($20k).
- Constraints: zero cost (GCP $150 credits), local-first, 19-day build (Aug 12-31), AI-assisted
  dev with full attribution (this file + repo history + prompts/ dir).
- Success = working demo on video: upload 3 NF-e's + 1 USDC invoice, see ledger + PTAX valuation
  + payment link + settlement confirm + accountant CSV, and a prompt-injection attempt refused.

## spec/tool-extract.md
- Name: extract_invoice(attachment) -> Invoice
- Input: NF-e XML, NF-e PDF, or photo of DANFE (Gemini vision), or email forward.
- Output: {docType, issuer{cnpj,name}, number, series, issuedAt, items[{code,desc,cfop,ncm,amount}],
  total, taxes, paymentMethod, barcode/accessKey}
- Rules: unknown fields -> null (never guess); duplicate accessKey -> error "already booked";
  totals must match sum(items) within R$0.01 else flag "inconsistent" (do not book).
- Tests: fixtures = 1 real NF-e XML sample + 1 DANFE PDF + 1 photo; golden outputs pinned.

## spec/tool-ledger.md
- Name: book_invoice(entry) -> LedgerEntry; reconcile(period) -> Report
- Every entry: {id, accessKey, date, valueBRL, valueUSDC?, ptaxRate?, ptaxDate?, status}
- USDC invoices valued at BCB PTAX close for the settlement date (olinda.bcb.gov.br PTAX API,
  verified working 2026-08-12). Same-day only; missing PTAX -> pending valuation, never invented.
- Month-close: append-only, hash-chained (each entry carries prev hash) -> accountant CSV (PT-BR).
- Rules: no deletion/editing after book; export is byte-identical on re-run.

## spec/tool-pay.md
- Name: request_payment(invoice, wallet) -> PaymentLink; verify_payment(ref) -> Status
- Payment link: Solana Pay-style URL with UNIQUE reference key (uuid, not memo) binding the
  invoice; amount + asset (USDC) explicit; expiry 24h.
- Verify: on-chain lookup of reference key -> PAID/UNDERPAID/WRONG_ASSET/EXPIRED (never "paid"
  from a memo or label — forgeable).
- Custody: T0 read + T1 build only. No signing key in agent; payout proposal -> human approval SOP.
- Mock mode for devnet/demo; real rail = devnet during hackathon (no real funds).

## spec/security.md
- Attack surface: invoice text/attachments, webhook bodies, Telegram messages = UNTRUSTED.
- Fail-closed: any ambiguity -> refuse + report to operator; no silent fallbacks for money paths.
- Prompt injection: tests with transcripts (injection tries to change payout wallet / amounts /
  claim "admin override") — 3 documented attempts, all refused.
- Approval boundary: payout wallets config-owned; caps per day; approval required above cap.

## spec/demo.md
- 2-4 min video: (1) intro 15s, (2) intake demo 45s, (3) ledger+PTAX 45s, (4) payment+verify 45s,
  (5) injection refusal 20s, (6) accountant export 15s, (7) arch diagram 15s.
- EN narration, PT-BR UI. Repo: README + arch diagram + this spec dir + prompts/ dir.

## Build order (Aug 12-31)
1. [DONE] Research: PTAX API verified; x402 spec (moved to x402-foundation/x402); ADK docs live.
2. Skeleton repo (local): pyproject (adk), tools/, tests/, prompts/, docs/.
3. extract_invoice with fixtures (3-4 days).
4. ledger + PTAX (2 days).
5. pay rail mock->devnet (3 days).
6. Telegram channel + approval SOP (2 days).
7. Injection tests + hardening (2 days).
8. UX polish + arch doc + demo video (3 days).
9. Submit by Aug 31 21:00 GMT-3.

## Decisions pending operator (blocking only at their step)
- Devpost registration (email/Google) — needed to submit.
- Project name + PT-BR vs EN UI.
- Whether to also target ETHOnline Continuity with the same base (Sep) — yes per ETHONLINE_PLAN.md.
