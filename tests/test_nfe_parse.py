"""NF-e XML parse tests (no network)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

from fixtures.nfe_v400 import NFe_V400
from nfe_agent.core.nfe_parse import parse_nfe_xml
from nfe_agent.core.rules import RuleError, validate_totals


def test_parse_valid_nfe():
    inv = parse_nfe_xml(NFe_V400.encode("utf-8"))
    assert inv.access_key == "35260812345678000190550010000000011000000019"
    assert inv.issuer_cnpj == "12345678000190"
    assert inv.number == "1" and inv.series == "1"
    assert inv.total == 3000.00
    assert len(inv.items) == 2
    assert inv.items[0]["amount"] == 2500.00
    assert inv.items[1]["desc"] == "HOSPEDAGEM DE SISTEMA"
    validate_totals(inv)  # 2500 + 500 == 3000


def test_parse_rejects_non_nfe():
    try:
        parse_nfe_xml(b"<foo><bar/></foo>")
        assert False, "should have raised"
    except RuleError:
        pass


def test_parse_rejects_bad_access_key():
    # 43 ones with a WRONG check digit (correct DV for 43 ones is 2)
    bad = NFe_V400.replace("35260812345678000190550010000000011000000019", "1" * 43 + "0")
    try:
        parse_nfe_xml(bad.encode("utf-8"))
        assert False, "should have raised"
    except RuleError:
        pass


def test_access_key_check_digit():
    from nfe_agent.core.rules import _check_digit_ok
    assert _check_digit_ok("35260812345678000190550010000000011000000019")
    assert not _check_digit_ok("35260812345678000190550010000000011000000018")
    assert _check_digit_ok("1" * 43 + "2")   # 43 ones -> DV 2
    assert not _check_digit_ok("1" * 43 + "0")
