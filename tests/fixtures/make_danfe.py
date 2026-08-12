"""Generate a DANFE-like invoice PNG fixture (same data as the XML fixture)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIXTURE = Path(__file__).parent


def make_danfe_png(path: Path | None = None) -> Path:
    out = path or (FIXTURE / "danfe_fixture.png")
    img = Image.new("RGB", (900, 1200), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 18)
        font_b = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 20)
    except OSError:
        font = font_b = ImageFont.load_default()

    d.rectangle([0, 0, 900, 60], fill="black")
    d.text((20, 18), "DANFE - Documento Auxiliar da Nota Fiscal Eletronica", fill="white", font=font_b)
    d.text((20, 80), "EMPRESA TESTE LTDA  -  CNPJ: 12.345.678/0001-90", fill="black", font=font)
    d.text((20, 110), "NFe: 3526 0812 3456 7800 0190 5500 1000 0000 0110 0000 0019", fill="black", font=font)
    d.text((20, 140), "Chave de acesso: 35260812345678000190550010000000011000000019", fill="black", font=font)
    d.text((20, 170), "Numero: 1  Serie: 1  Emissao: 10/08/2026", fill="black", font=font)
    d.line([20, 200, 880, 200], fill="black")
    d.text((20, 210), "Item | Codigo | Descricao | CFOP | NCM | Valor", fill="black", font=font_b)
    d.text((20, 240), "1    | P001   | PRESTACAO DE SERVICO DE DESENVOLVIMENTO | 5949 | 00000000 | 2500.00", fill="black", font=font)
    d.text((20, 270), "2    | P002   | HOSPEDAGEM DE SISTEMA | 5949 | 00000000 | 500.00", fill="black", font=font)
    d.line([20, 300, 880, 300], fill="black")
    d.text((20, 310), "VALOR TOTAL DA NOTA: R$ 3000.00", fill="black", font=font_b)
    d.text((20, 340), "Pagamento: 01 - Dinheiro", fill="black", font=font)
    d.line([20, 370, 880, 370], fill="black")
    d.text((20, 380), "DESTINATARIO: CLIENTE TESTE - CPF: 987.654.321-00", fill="black", font=font)
    img.save(out)
    return out


if __name__ == "__main__":
    print(make_danfe_png())
