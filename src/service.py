from typing import List, Dict, Optional
from models import Product, StockTransaction, TransactionType
from notifiers import Notifier


class InventoryService:
    """ระบบจัดการคลังสินค้า และทำหน้าที่เป็น Subject ใน Observer Pattern สำหรับส่งการแจ้งเตือนสต็อก"""

    def __init__(self, notifiers: Optional[List[Notifier]] = None) -> None:
        self.products: Dict[int, Product] = {}
        self.transactions: List[StockTransaction] = []
        # Dependency Injection & Observer List: รับ Notifiers ผ่าน constructor
        self._notifiers: List[Notifier] = list(notifiers) if notifiers is not None else []
        self._next_tx_id: int = 1

    def attach_notifier(self, notifier: Notifier) -> None:
        """เพิ่ม Notifier (Observer) เข้าไปในระบบ"""
        if notifier not in self._notifiers:
            self._notifiers.append(notifier)

    def detach_notifier(self, notifier: Notifier) -> None:
        """ลบ Notifier (Observer) ออกจากระบบ"""
        if notifier in self._notifiers:
            self._notifiers.remove(notifier)

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าเข้าสู่ระบบ"""
        self.products[product.id] = product

    def set_threshold(self, product_id: int, new_threshold: int) -> None:
        """ตั้งค่า threshold ของสินค้า"""
        if new_threshold < 0:
            raise ValueError("Threshold ต้องมากกว่าหรือเท่ากับ 0")
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")

        self.products[product_id].threshold = new_threshold

    def receive_stock(self, product_id: int, quantity: int) -> StockTransaction:
        """บันทึกการรับสินค้าเข้าสต็อก"""
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าที่รับต้องมากกว่า 0")
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")

        product = self.products[product_id]
        stock_before = product.quantity
        product.quantity += quantity
        stock_after = product.quantity

        tx = StockTransaction(
            transaction_id=self._next_tx_id,
            product_id=product_id,
            type=TransactionType.RECEIVE,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=stock_after,
        )
        self._next_tx_id += 1
        self.transactions.append(tx)
        return tx

    def issue_stock(self, product_id: int, quantity: int) -> StockTransaction:
        """บันทึกการจ่ายสินค้าออกจากสต็อก พร้อมแจ้งเตือน Observer หากสต็อกเข้าเงื่อนไข"""
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าที่จ่ายต้องมากกว่า 0")
        if product_id not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")

        product = self.products[product_id]
        if quantity > product.quantity:
            raise ValueError("สต็อกไม่เพียงพอ")

        stock_before = product.quantity
        product.quantity -= quantity
        stock_after = product.quantity

        tx = StockTransaction(
            transaction_id=self._next_tx_id,
            product_id=product_id,
            type=TransactionType.ISSUE,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=stock_after,
        )
        self._next_tx_id += 1
        self.transactions.append(tx)

        if product.quantity <= product.threshold:
            self._notify_observers(product)

        return tx

    def _notify_observers(self, product: Product) -> None:
        """Observer Pattern: บรอดแคสต์การแจ้งเตือนไปยัง Observer ทุกตัวโดยไม่ขึ้นกับ concrete class"""
        msg = (
            f"สินค้า: {product.name}\n"
            f"สต็อกคงเหลือ: {product.quantity}\n"
            f"Threshold: {product.threshold}\n"
            f"ประเภท: LOW_STOCK"
        )
        for notifier in self._notifiers:
            try:
                notifier.send(msg)
            except Exception as e:
                print(f"[Warning] ส่งการแจ้งเตือนล้มเหลว: {e}")


class ReportService:
    """ระบบรายงานและคำนวณมูลค่าสต็อก"""

    def __init__(self, inventory_service: InventoryService) -> None:
        self.inventory_service = inventory_service

    def get_stock_value_report(self) -> Dict[str, float]:
        """คำนวณและสรุปมูลค่าสต็อกแยกตามหมวดหมู่ พร้อมยอดรวมทั้งหมด"""
        report: Dict[str, float] = {}
        total_value: float = 0.0

        for product in self.inventory_service.products.values():
            if product.unit_price is None:
                raise ValueError(f"สินค้า '{product.name}' ไม่มีราคาต้นทุน")

            product_val = product.quantity * product.unit_price
            report[product.category] = round(
                report.get(product.category, 0.0) + product_val, 2
            )
            total_value += product_val

        report["TOTAL"] = round(total_value, 2)
        return report