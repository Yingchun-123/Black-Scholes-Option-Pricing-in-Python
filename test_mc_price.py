import math
import pytest
from mc_price import mc_price
from option import Option, Call, Put
from closed_form import closed_form_price

def rel_err(a, b):
    denom = max(1.0, abs(b))
    return abs(a - b) / denom

def test_mc_matches_bs_call_medium_n():
    # 选一个典型参数，样本数适中，运行速度与精度兼顾
    opt = Call(100, 120, 0.04, 0.2, 2.0)
    bs_call = closed_form_price(opt, is_call=True)
    mc_call = mc_price(opt, n=200_000, seed=123)
    assert rel_err(mc_call, bs_call) < 0.02  # 2% 以内

# ---------- 2) 与闭式解一致性（Put） ----------
def test_mc_matches_bs_put_medium_n():
    opt = Put(100, 120, 0.04, 0.2, 2.0)
    bs = closed_form_price(opt, is_call=False)
    mc = mc_price(opt, n=200_000, seed=456)
    assert rel_err(mc, bs) < 0.02

def test_mc_monotonic_in_S0_call():
    v_low  = mc_price(Call(90, 100, 0.03, 0.2, 1.5), n=80_000, seed=11)
    v_high = mc_price(Call(110,100, 0.03, 0.2, 1.5), n=80_000, seed=11)
    assert v_high >= v_low
