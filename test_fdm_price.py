import math
import pytest
from fdm_price import fdm_price
from closed_form import closed_form_price
from option import Option,Call,Put

def rel_err(a, b):
    denom = max(1.0, abs(b))
    return abs(a - b) / denom


def test_fdm_matches_bs():
    # Call
    opt_call = Call(100, 100, 0.05, 0.20, 1.0)
    bs_call  = closed_form_price(opt_call, is_call=True)
    fdm_call = fdm_price(opt_call, N=400, M=800)
    assert rel_err(fdm_call, bs_call) < 0.02

    # Put
    opt_put = Put(100, 100, 0.05, 0.20, 1.0)
    bs_put  = closed_form_price(opt_put, is_call=False)
    fdm_put = fdm_price(opt_put, N=400, M=800)
    assert rel_err(fdm_put, bs_put) < 0.02

def test_fdm_monotonicity_call():
    r, sigma, T = 0.03, 0.20, 1.5

    c_lowS  = fdm_price(Call( 90, 100, r, sigma, T), N=400, M=800)
    c_highS = fdm_price(Call(110, 100, r, sigma, T), N=400, M=800)
    assert c_highS >= c_lowS

    c_lowK  = fdm_price(Call(100,  90, r, sigma, T), N=400, M=800)
    c_highK = fdm_price(Call(100, 110, r, sigma, T), N=400, M=800)
    assert c_lowK >= c_highK

