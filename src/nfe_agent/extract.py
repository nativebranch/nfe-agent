"""Multimodal invoice extraction: deterministic XML path + Gemini vision for PDF/photo."""
from __future__ import annotations

import json
from pathlib import Path

from .core.nfe_parse import parse_nfe_xml
from .core.rules import Invoice, RuleError, validate_access_key, validate_totals
from .llm import default_model, get_client

EXTRACT_PROMPT = """You extract structured data from Brazilian NF-e invoices (DANFE).
Return ONLY a JSON object, no markdown, with exactly these fields:
{
  "access_key": "44-digit key shown as 'Chave de Acesso' (digits only)",
  "issuer_cnpj": "digits only",
  "number": "nNF",
  "series": "serie",
  "issued_at": "ISO date (yyyy-mm-dd)",
  "items": [{"code": "cProd", "desc": "xProd", "cfop": "CFOP", "ncm": "NCM", "amount": 0.0}],
  "total": 0.0,
  "payment_method": "01|02|... or null"
}
Rules: unknown -> null/empty; do NOT invent values; amounts as numbers with 2 decimals."""


def extract_invoice_from_document(path: str | Path) -> Invoice:
    """Extract from PDF or image via Gemini vision, then validate fail-closed."""
    p = Path(path)
    if not p.exists():
        raise RuleError(f"file not found: {p}")
    client = get_client()
    import google.genai.types as types
    resp = client.models.generate_content(
        model=default_model(),
        contents=[
            types.Part.from_bytes(data=p.read_bytes(), mime_type=_mime(p)),
            EXTRACT_PROMPT,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0,
        ),
    )
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError as e:
        raise RuleError(f"LLM returned invalid JSON: {e}")
    return _invoice_from_dict(data)


def _invoice_from_dict(d: dict) -> Invoice:
    access_key = str(d.get("access_key") or "").strip()
    validate_access_key(access_key)
    inv = Invoice(
        access_key=access_key,
        issuer_cnpj=str(d.get("issuer_cnpj") or ""),
        number=str(d.get("number") or ""),
        series=str(d.get("series") or ""),
        issued_at=str(d.get("issued_at") or ""),
        items=[{"code": str(i.get("code") or ""), "desc": str(i.get("desc") or ""),
                "cfop": str(i.get("cfop") or ""), "ncm": str(i.get("ncm") or ""),
                "amount": float(i.get("amount") or 0.0)} for i in (d.get("items") or [])],
        total=float(d.get("total") or 0.0),
        payment_method=d.get("payment_method"),
    )
    validate_totals(inv)
    return inv


def _mime(p: Path) -> str:
    return {"pdf": "application/pdf", "png": "image/png", "jpg": "image/jpeg",
            "jpeg": "image/jpeg", "webp": "image/webp"}.get(p.suffix.lower().lstrip("."), "application/octet-stream")
