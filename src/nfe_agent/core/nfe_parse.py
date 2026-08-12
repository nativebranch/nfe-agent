"""NF-e XML parser (deterministic path; Gemini vision only needed for PDF/photo)."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from .rules import Invoice, RuleError, validate_access_key

NS = {"nfe": "http://www.portalfiscal.inf.br/nfe"}


def parse_nfe_xml(xml_bytes: bytes) -> Invoice:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise RuleError(f"unparseable XML: {e}")
    inf = root.find(".//nfe:infNFe", NS)
    if inf is None:
        raise RuleError("not an NF-e document (no infNFe)")
    ide = inf.find("nfe:ide", NS)
    emit = inf.find("nfe:emit", NS)
    total = inf.find(".//nfe:total/nfe:ICMSTot", NS)

    def txt(el, tag):
        node = el.find(f"nfe:{tag}", NS) if el is not None else None
        return node.text.strip() if node is not None and node.text else ""

    access_key = inf.get("Id", "")[3:] if inf.get("Id") else ""
    validate_access_key(access_key)
    items = []
    for det in inf.findall(".//nfe:det", NS):
        prod = det.find("nfe:prod", NS)
        items.append({
            "code": txt(prod, "cProd"),
            "desc": txt(prod, "xProd"),
            "cfop": txt(prod, "CFOP"),
            "ncm": txt(prod, "NCM"),
            "amount": float(txt(prod, "vProd") or 0.0),
        })
    return Invoice(
        access_key=access_key,
        issuer_cnpj=txt(emit, "CNPJ"),
        number=txt(ide, "nNF"),
        series=txt(ide, "serie"),
        issued_at=txt(ide, "dhEmi") or txt(ide, "dEmi"),
        items=items,
        total=float(txt(total, "vNF") or 0.0),
        payment_method=txt(inf.find("nfe:pag", NS), "tPag") or None,
    )
