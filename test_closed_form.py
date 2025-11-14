import math
import pytest
from closed_form import closed_form_price
from option import Option

def test_bs_call_known_value():
    opt = Option(100, 100, 0.05, 0.2, 1.0)
    price = closed_form_price(opt,is_call=True)
    assert price == pytest.approx(10.4506, rel=0, abs=1e-3)

def test_bs_put_known_value():
    opt = Option(100, 100, 0.05, 0.2, 1.0)
    price = closed_form_price(opt,is_call=False)
    assert price == pytest.approx(5.5735, rel=0, abs=1e-3)

def test_monotonicity_call_in_S0_and_K():
    # S0 ↑ → Call ↑
    c1 = closed_form_price(Option(90, 100, 0.03, 0.2, 1.5), is_call=True)
    c2 = closed_form_price(Option(110, 100, 0.03, 0.2, 1.5),is_call=True)
    assert c2 >= c1

    # K ↑ → Call ↓
    ck1 = closed_form_price(Option(100, 90, 0.03, 0.2, 1.5),is_call=True)
    ck2 = closed_form_price(Option(100, 110, 0.03, 0.2, 1.5),is_call=True)
    assert ck1 >= ck2
