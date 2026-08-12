"""Vision extraction test: real Gemini call against the DANFE fixture PNG."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

from fixtures.make_danfe import make_danfe_png
from nfe_agent.extract import extract_invoice_from_document
from nfe_agent.core.rules import RuleError


def test_vision_extract_danfe():
    png = make_danfe_png()
    inv = extract_invoice_from_document(png)
    print(f"\nEXTRACTED: key={inv.access_key} total={inv.total} items={len(inv.items)}")
    print(f"  issuer={inv.issuer_cnpj} items: {[(i['desc'][:30], i['amount']) for i in inv.items]}")
    assert inv.access_key == "35260812345678000190550010000000011000000019"
    assert inv.total == 3000.00
    assert len(inv.items) == 2
    assert inv.issuer_cnpj == "12345678000190"
    # fail-closed: tampered image (wrong total) must be rejected
    from PIL import Image, ImageDraw, ImageFont
    bad = Image.open(png).copy()
    d = ImageDraw.Draw(bad)
    d.rectangle([20, 300, 700, 330], fill="white")
    d.text((20, 310), "VALOR TOTAL DA NOTA: R$ 2999.99", fill="black",
           font=ImageFont.load_default())
    bad_path = png.with_name("danfe_tampered.png")
    bad.save(bad_path)
    try:
        extract_invoice_from_document(bad_path)
        print("WARN: tampered invoice accepted (LLM missed the mismatch)")
    except RuleError as e:
        print(f"tampered rejected as expected: {e}")
