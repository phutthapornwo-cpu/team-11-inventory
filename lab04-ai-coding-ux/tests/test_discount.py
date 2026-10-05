import pytest
from discount import apply_discount, bulk_total, average_price, cheapest_n

# --- Test apply_discount ---
def test_apply_discount_normal():
    assert apply_discount(100.0, 10.0) == 90.0
    assert apply_discount(200.0, 25.0) == 150.0

def test_apply_discount_zero_or_full():
    assert apply_discount(100.0, 0.0) == 100.0
    assert apply_discount(100.0, 100.0) == 0.0

def test_apply_discount_invalid_input():
    with pytest.raises(ValueError):
        apply_discount(-50.0, 10.0)
    with pytest.raises(ValueError):
        apply_discount(100.0, 150.0)

# --- Test bulk_total ---
def test_bulk_total():
    assert bulk_total([100.0, 200.0, 300.0], 10.0) == 540.0
    assert bulk_total([], 10.0) == 0.0

# --- Test average_price ---
def test_average_price():
    assert average_price([10.0, 20.0, 30.0]) == 20.0
    assert average_price([]) == 0.0

# --- Test cheapest_n ---
def test_cheapest_n():
    prices = [50.0, 10.0, 30.0, 20.0, 40.0]
    assert cheapest_n(prices, 3) == [10.0, 20.0, 30.0]
    assert cheapest_n(prices, 1) == [10.0]
    assert cheapest_n([], 3) == []