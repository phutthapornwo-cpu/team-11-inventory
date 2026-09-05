from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Category:
    """หมวดหมู่สินค้าในระบบคลัง"""

    name: str


@dataclass
class Product:
    """ข้อมูลสินค้าและสถานะสต็อก"""

    code: str
    name: str
    category: Category
    unit_price: float
    quantity: int = 0
    threshold: int = 0

    def __post_init__(self) -> None:
        """ตรวจสอบความถูกต้องของข้อมูลสินค้าเริ่มต้น"""
        if self.quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")
        if self.threshold < 0:
            raise ValueError("threshold ต้องไม่ติดลบ")
        if self.unit_price < 0:
            raise ValueError("ราคาต่อหน่วยต้องไม่ติดลบ")

    def increase_stock(self, quantity: int) -> None:
        """เพิ่มจำนวนสินค้าในคลัง"""
        if quantity <= 0:
            raise ValueError("จำนวนรับเข้าต้องมากกว่า 0")
        self.quantity += quantity

    def decrease_stock(self, quantity: int) -> None:
        """ลดจำนวนสินค้าในคลังเมื่อมีการจ่ายออก"""
        if quantity <= 0:
            raise ValueError("จำนวนจ่ายออกต้องมากกว่า 0")
        if quantity > self.quantity:
            raise ValueError("จำนวนคงเหลือไม่พอ")
        self.quantity -= quantity

    def is_low_stock(self) -> bool:
        """ตรวจสอบว่าสต็อกต่ำกว่า threshold หรือไม่"""
        return self.quantity < self.threshold

    def inventory_value(self) -> float:
        """คำนวณมูลค่าสต็อกของสินค้ารายการนี้"""
        return self.quantity * self.unit_price


@dataclass(frozen=True)
class StockTransaction:
    """รายการเคลื่อนไหวรับ/จ่ายสินค้า"""

    product_code: str
    quantity: int
    transaction_type: Literal["IN", "OUT"]
