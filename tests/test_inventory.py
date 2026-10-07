import pytest
from inventory import Inventory


def test_low_stock_all_above_threshold():
    # 1. สินค้าทุกรายการมากกว่า threshold -> คืน list ว่าง
    inv = Inventory()
    inv.add_item("Apple", 10)
    inv.add_item("Banana", 20)
    assert inv.low_stock_items(5) == []


def test_low_stock_exact_threshold():
    # 2. มีสินค้าเท่ากับ threshold พอดี -> ต้องถูกนับรวมด้วย
    inv = Inventory()
    inv.add_item("Apple", 5)
    inv.add_item("Banana", 10)
    assert inv.low_stock_items(5) == ["Apple"]


def test_low_stock_sorted_by_name():
    # 3. มีสินค้าหลายรายการเข้าเกณฑ์ -> ผลลัพธ์ต้องเรียงตามชื่อ (A-Z)
    inv = Inventory()
    inv.add_item("Orange", 2)
    inv.add_item("Banana", 3)
    inv.add_item("Apple", 1)
    assert inv.low_stock_items(5) == ["Apple", "Banana", "Orange"]


def test_low_stock_empty_inventory():
    # 4. คลังสินค้าว่าง -> คืน list ว่าง
    inv = Inventory()
    assert inv.low_stock_items(5) == []


def test_low_stock_threshold_zero():
    # 5. threshold เป็น 0 -> คืนเฉพาะสินค้าที่เหลือ 0
    inv = Inventory()
    inv.add_item("Apple", 0)
    inv.add_item("Banana", 2)
    assert inv.low_stock_items(0) == ["Apple"]


def test_low_stock_negative_threshold():
    # 6. threshold ติดลบ -> กำหนดพฤติกรรมเอง (เช่น คืน list ว่าง)
    inv = Inventory()
    inv.add_item("Apple", 0)
    assert inv.low_stock_items(-1) == []