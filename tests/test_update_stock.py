import pytest

import update_stock


@pytest.fixture(autouse=True)
def reset_inventory():
    """รีเซ็ต inventory ก่อนแต่ละ test"""
    update_stock.inventory.clear()
    update_stock.inventory.update({
        "P001": 50,
        "P002": 20,
    })


def test_update_stock_in_success():
    result = update_stock.update_stock("P001", "in", 10)

    assert result["success"] is True
    assert result["new_balance"] == 60
    assert update_stock.inventory["P001"] == 60


def test_update_stock_out_success():
    result = update_stock.update_stock("P001", "out", 10)

    assert result["success"] is True
    assert result["new_balance"] == 40
    assert update_stock.inventory["P001"] == 40


def test_update_stock_invalid_amount():
    result = update_stock.update_stock("P001", "in", 0)

    assert result["success"] is False
    assert result["new_balance"] is None


def test_update_stock_product_not_found():
    result = update_stock.update_stock("P999", "in", 10)

    assert result["success"] is False
    assert result["new_balance"] is None


def test_update_stock_out_more_than_balance():
    result = update_stock.update_stock("P001", "out", 100)

    assert result["success"] is False
    assert result["new_balance"] == 50
    assert update_stock.inventory["P001"] == 50


def test_update_stock_invalid_action():
    result = update_stock.update_stock("P001", "delete", 10)

    assert result["success"] is False
    assert result["new_balance"] is None
    assert update_stock.inventory["P001"] == 50