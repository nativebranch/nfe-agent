"""PTAX client: official Banco Central do Brasil exchange-rate API (verified live)."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class PTAXRate:
    currency: str
    date: str          # ISO yyyy-mm-dd
    buy: float
    sell: float

    @property
    def mid(self) -> float:
        return round((self.buy + self.sell) / 2.0, 4)


class PTAXError(Exception):
    pass


class PTAXClient:
    BASE = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"

    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def quote(self, currency: str = "USD", date: str | None = None) -> PTAXRate:
        """Date format dd-mm-yyyy (BCB convention). Returns the day's bulletin rate."""
        from datetime import date as _date
        d = date or _date.today().strftime("%d-%m-%Y")
        url = (
            self.BASE
            + "CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)"
            + f"?@moeda='{currency}'&@dataCotacao='{d}'&$top=1&$format=json"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "nfe-agent/0.1"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            payload = json.loads(r.read().decode("utf-8"))
        rows = payload.get("value") or []
        if not rows:
            raise PTAXError(f"no PTAX rate for {currency} on {d} (non-business day?)")
        row = rows[0]
        iso = d[-4:] + "-" + d[3:5] + "-" + d[0:2]
        return PTAXRate(currency, iso, float(row["cotacaoCompra"]), float(row["cotacaoVenda"]))
