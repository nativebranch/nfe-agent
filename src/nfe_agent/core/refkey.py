"""Reference keys: unique, unforgeable bindings between an invoice and a payment.

A payment is only 'paid' when the on-chain transaction carries THIS key in a
machine-checkable field (transfer memo is forgeable by the payer, so we use a
reference key embedded in a Solana Pay request / x402 header instead).
"""
from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass

KEY_NAMESPACE = uuid.UUID("6f1e9c3a-2b4d-4e5f-8a9b-0c1d2e3f4a5b")


def new_reference_key(invoice_id: str) -> str:
    """Deterministic-but-unique key bound to the invoice id (uuid5)."""
    return str(uuid.uuid5(KEY_NAMESPACE, invoice_id))


def is_valid_reference_key(key: str) -> bool:
    """A valid key is a well-formed uuid5 (namespace is not recoverable from the
    string form, so we check format + version 5)."""
    try:
        u = uuid.UUID(key)
        return u.version == 5
    except (ValueError, AttributeError):
        return False


@dataclass(frozen=True)
class Settlement:
    key: str
    asset: str          # e.g. "USDC"
    amount: float
    txid: str
    confirmed: bool


def verify_settlement(key: str, tx_payload: dict) -> Settlement:
    """Check a transaction payload against the reference key. Fail-closed:
    ANY inconsistency -> confirmed=False (never a partial 'paid')."""
    if not is_valid_reference_key(key):
        return Settlement(key, "", 0.0, "", False)
    ref = tx_payload.get("reference", "")
    if ref != key:
        return Settlement(key, "", 0.0, "", False)
    asset = tx_payload.get("asset", "")
    amount = float(tx_payload.get("amount", 0.0))
    txid = tx_payload.get("txid", "")
    confirmed = bool(txid) and asset.upper() in {"USDC", "USDT", "USDG"}
    return Settlement(key, asset.upper(), amount, txid, confirmed)


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
