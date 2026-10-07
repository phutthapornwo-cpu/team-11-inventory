import pytest

from inventory import Inventory  # <--- เพิ่มบรรทัดนี้


# --- Test เดิมสำหรับ low_stock_items ---
def test_all_items_above_threshold():
    inv = Inventory({'apple': 10, 'banana': 20})
    assert inv.low_stock_items(5) == []

def test_item_equal_to_threshold():
    inv = Inventory({'apple': 5, 'banana': 10})
    assert inv.low_stock_items(5) == ['apple']

def test_multiple_items_sorted():
    inv = Inventory({'banana': 3, 'apple': 2, 'cherry': 10})
    assert inv.low_stock_items(5) == ['apple', 'banana']

def test_empty_inventory():
    inv = Inventory({})
    assert inv.low_stock_items(5) == []

def test_threshold_zero():
    inv = Inventory({'apple': 0, 'banana': 5})
    assert inv.low_stock_items(0) == ['apple']

def test_negative_threshold():
    inv = Inventory({'apple': 5, 'banana': 10})
    assert inv.low_stock_items(-1) == []

# --- Test สำหรับ sell (ขั้นที่ 4) ---
def test_sell_success():
    inv = Inventory({'apple': 10})
    inv.sell('apple', 3)
    assert inv.items['apple'] == 7

def test_sell_exact_remaining():
    inv = Inventory({'apple': 5})
    inv.sell('apple', 5)
    assert inv.items['apple'] == 0

def test_sell_zero_or_negative():
    inv = Inventory({'apple': 10})
    with pytest.raises(ValueError):
        inv.sell('apple', 0)
    with pytest.raises(ValueError):
        inv.sell('apple', -2)

def test_sell_exceeds_stock():
    inv = Inventory({'apple': 3})
    with pytest.raises(ValueError):
        inv.sell('apple', 5)

def test_sell_non_existent_item():
    inv = Inventory({'apple': 10})
    with pytest.raises(KeyError):
        inv.sell('banana', 1)

def test_sell_invalid_type():
    inv = Inventory({'apple': 10})
    with pytest.raises(TypeError):
        inv.sell('apple', "two")