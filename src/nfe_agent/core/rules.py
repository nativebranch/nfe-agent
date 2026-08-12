"""Business rules: fail-closed validation for invoice intake and booking."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Invoice:
    access_key: str
    issuer_cnpj: str
    number: str
    series: str
    issued_at: str
    items: list[dict]
    total: float
    payment_method: str | None = None


class RuleError(Exception):
    """Any rule violation: caller must refuse to book (fail-closed)."""


def validate_totals(inv: Invoice, tolerance: float = 0.01) -> None:
    items_sum = round(sum(float(i.get("amount", 0.0)) for i in inv.items), 2)
    if abs(items_sum - round(float(inv.total), 2)) > tolerance:
        raise RuleError(
            f"total {inv.total} != sum(items) {items_sum} — inconsistent, refusing to book"
        )


def validate_access_key(access_key: str) -> None:
    if not (access_key.isdigit() and len(access_key) == 44):
        raise RuleError(f"invalid NF-e access key (len={len(access_key)})")
    if not _check_digit_ok(access_key):
        raise RuleError(f"access key {access_key} fails check-digit validation")


def _check_digit_ok(key: str) -> bool:
    """Official NF-e access-key check digit: weights 2..9 cycling from the right
    over the first 43 digits; rem 0/1 -> DV 0, else 11-rem."""
    body = key[:43]
    total = 0
    weight = 2
    for ch in reversed(body):
        total += int(ch) * weight
        weight = 2 if weight == 9 else weight + 1
    rem = total % 11
    dv = 0 if rem in (0, 1) else 11 - rem
    return dv == int(key[43])


def check_duplicate(access_key: str, known_keys: set[str]) -> None:
    if access_key in known_keys:
        raise RuleError(f"access key {access_key} already booked — duplicate")


def check_amount(amount: float, cap: float, currency: str = "USDC") -> None:
    if amount <= 0:
        raise RuleError("amount must be positive")
    if amount > cap:
        raise RuleError(f"amount {amount} {currency} exceeds operator cap {cap} — needs approval")
