from __future__ import annotations

from typing import Iterable

from src.models import Product, StockTransaction
from src.notifiers import Notifier


class InventoryService:
    """บริการจัดการสต็อกสินค้าและรายงานมูลค่า"""

    def __init__(
        self,
        notifiers: Iterable[Notifier],
        products: dict[str, Product] | None = None,
    ) -> None:
        """เตรียม service พร้อม dependency และข้อมูลสินค้าเริ่มต้น"""
        self._notifiers = list(notifiers)
        self._products: dict[str, Product] = products or {}

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าระบบ"""
        if product.code in self._products:
            raise ValueError("รหัสสินค้าซ้ำ")
        self._products[product.code] = product

    def record_stock_in(self, product_code: str, quantity: int) -> StockTransaction:
        """บันทึกรับสินค้าเข้าและอัปเดตสต็อกทันที"""
        product = self._get_product_or_raise(product_code)
        product.increase_stock(quantity)
        return StockTransaction(product_code=product_code, quantity=quantity, transaction_type="IN")

    def record_stock_out(self, product_code: str, quantity: int) -> StockTransaction:
        """บันทึกจ่ายสินค้าออกและแจ้งเตือนเมื่อสต็อกต่ำ"""
        product = self._get_product_or_raise(product_code)
        product.decrease_stock(quantity)

        if product.is_low_stock():
            for notifier in self._notifiers:
                notifier.send_low_stock_alert(product)

        return StockTransaction(product_code=product_code, quantity=quantity, transaction_type="OUT")

    def get_product(self, product_code: str) -> Product:
        """ดึงข้อมูลสินค้าตามรหัส"""
        return self._get_product_or_raise(product_code)

    def report_inventory_value_by_category(self) -> dict[str, float]:
        """สรุปมูลค่าสต็อกรวมแยกตามหมวดหมู่"""
        totals: dict[str, float] = {}
        for product in self._products.values():
            category_name = product.category.name
            totals[category_name] = totals.get(category_name, 0.0) + product.inventory_value()
        return totals

    def _get_product_or_raise(self, product_code: str) -> Product:
        if product_code not in self._products:
            raise ValueError("ไม่พบสินค้า")
        return self._products[product_code]
