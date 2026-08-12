"""Ledger: append-only, hash-chained receivables book with PTAX valuation."""
from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from .refkey import sha256_hex


@dataclass
class Entry:
    entry_id: str
    access_key: str          # NF-e access key (44 digits) or invoice ref
    date: str                # ISO date (settlement/issue date)
    value_brl: float
    value_usdc: float | None = None
    ptax_rate: float | None = None
    status: str = "booked"   # booked | pending_valuation | paid
    prev_hash: str = ""
    hash: str = ""

    def compute(self, prev_hash: str) -> "Entry":
        self.prev_hash = prev_hash
        body = json.dumps(
            [self.entry_id, self.access_key, self.date, self.value_brl,
             self.value_usdc, self.ptax_rate, self.status, self.prev_hash],
            sort_keys=True, default=str,
        )
        self.hash = sha256_hex(body)
        return self


class Ledger:
    def __init__(self) -> None:
        self.entries: list[Entry] = []

    def add(self, entry: Entry) -> Entry:
        prev = self.entries[-1].hash if self.entries else "GENESIS"
        entry.compute(prev)
        self.entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for e in self.entries:
            if e.prev_hash != prev:
                return False
            e.compute(e.prev_hash)  # recompute; hash must be stable
            prev = e.hash
        return True

    def to_csv(self) -> str:
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["id", "access_key", "date", "value_brl", "value_usdc",
                    "ptax_rate", "status", "hash"])
        for e in self.entries:
            w.writerow([e.entry_id, e.access_key, e.date, e.value_brl,
                        e.value_usdc or "", e.ptax_rate or "", e.status, e.hash])
        return buf.getvalue()
