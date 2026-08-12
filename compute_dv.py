import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from nfe_agent.core.rules import _check_digit_ok

# Independent reference implementation (weights 2..9 cycling from right)
def dv_of(body):
    total, weight = 0, 2
    for ch in reversed(body):
        total += int(ch) * weight
        weight = 2 if weight == 9 else weight + 1
    rem = total % 11
    return 0 if rem in (0, 1) else 11 - rem

for body in ["3526081234567800019055001000000001100000001",
             "1" * 43,
             "1234567890123456789012345678901234567890123"]:
    dv = dv_of(body)
    full = body + str(dv)
    print(f"body[:6]={body[:6]}... dv={dv} module_valid={_check_digit_ok(full)}")
