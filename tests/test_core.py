"""Core logic tests (no API keys, no network except one optional PTAX live check)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nfe_agent.core.refkey import new_reference_key, is_valid_reference_key, verify_settlement
from nfe_agent.core.ledger import Ledger, Entry
from nfe_agent.core.rules import (Invoice, validate_totals, validate_access_key,
                                  check_duplicate, check_amount, RuleError)
from nfe_agent.core.ptax import PTAXClient, PTAXError


def test_reference_key_roundtrip():
    k = new_reference_key("inv-1")
    assert is_valid_reference_key(k)
    assert new_reference_key("inv-1") == k          # deterministic
    assert not is_valid_reference_key("not-a-key")


def test_settlement_fail_closed():
    k = new_reference_key("inv-2")
    ok = verify_settlement(k, {"reference": k, "asset": "USDC", "amount": 10.0, "txid": "abc"})
    assert ok.confirmed and ok.amount == 10.0
    # forged memo / wrong key -> not confirmed
    bad = verify_settlement(k, {"reference": "forged", "asset": "USDC", "amount": 10.0, "txid": "x"})
    assert not bad.confirmed
    # wrong asset -> not confirmed
    bad2 = verify_settlement(k, {"reference": k, "asset": "SHIT", "amount": 10.0, "txid": "x"})
    assert not bad2.confirmed


def test_ledger_chain_and_csv():
    led = Ledger()
    led.add(Entry("e1", "12345678901234567890123456789012345678901234", "2026-08-10", 509.90))
    led.add(Entry("e2", "22345678901234567890123456789012345678901234", "2026-08-11", 100.00))
    assert led.verify_chain()
    csv_out = led.to_csv()
    assert "access_key" in csv_out and csv_out.count("\n") == 3
    # tamper detection: change an entry, chain breaks
    led.entries[0].value_brl = 999.0
    assert not led.verify_chain()


def test_rules_fail_closed():
    inv = Invoice(access_key="1" * 44, issuer_cnpj="123", number="1", series="1",
                  issued_at="2026-08-10", items=[{"amount": 10.0}, {"amount": 20.0}], total=30.0)
    validate_totals(inv)                      # ok
    inv.total = 31.0
    try:
        validate_totals(inv)
        assert False, "should have raised"
    except RuleError:
        pass
    try:
        validate_access_key("short")
        assert False
    except RuleError:
        pass
    check_duplicate("1" * 44, set())           # ok: not booked yet
    try:
        check_duplicate("2" * 44, {"2" * 44})  # already booked -> refuse
        assert False
    except RuleError:
        pass
    check_amount(5.0, 100.0)
    try:
        check_amount(500.0, 100.0)
        assert False
    except RuleError:
        pass


def test_ptax_live():
    """Live check against BCB (network). Skippable if offline."""
    try:
        r = PTAXClient().quote("USD", "11-08-2026")
        assert r.currency == "USD" and r.mid > 1.0
        print(f"PTAX live OK: {r.date} buy={r.buy} sell={r.sell}")
    except (PTAXError, OSError) as e:
        print(f"PTAX live skipped: {e}")
