from inventory import Inventory

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