import unittest

from src.models import Category, Product
from src.service import InventoryService


class SpyNotifier:
    def __init__(self) -> None:
        self.alerted_products: list[Product] = []

    def send_low_stock_alert(self, product: Product) -> None:
        self.alerted_products.append(product)


class TestInventoryService(unittest.TestCase):
    def setUp(self) -> None:
        self.notifier = SpyNotifier()
        self.service = InventoryService(notifiers=[self.notifier])
        self.product = Product(
            code="W001",
            name="สายไฟ 2.5 sq.mm",
            category=Category(name="ไฟฟ้า"),
            unit_price=10.0,
            quantity=20,
            threshold=15,
        )
        self.service.add_product(self.product)

    def test_stock_out_below_threshold_sends_alert(self) -> None:
        self.service.record_stock_out("W001", 8)

        self.assertEqual(self.service.get_product("W001").quantity, 12)
        self.assertEqual(len(self.notifier.alerted_products), 1)

    def test_stock_out_above_threshold_does_not_send_alert(self) -> None:
        product = Product(
            code="W002",
            name="สายไฟ 4 sq.mm",
            category=Category(name="ไฟฟ้า"),
            unit_price=12.0,
            quantity=50,
            threshold=15,
        )
        self.service.add_product(product)

        self.service.record_stock_out("W002", 10)

        self.assertEqual(self.service.get_product("W002").quantity, 40)
        self.assertEqual(len(self.notifier.alerted_products), 0)

    def test_reject_stock_out_when_not_enough(self) -> None:
        with self.assertRaisesRegex(ValueError, "จำนวนคงเหลือไม่พอ"):
            self.service.record_stock_out("W001", 21)

        self.assertEqual(self.service.get_product("W001").quantity, 20)

    def test_record_stock_in_updates_stock_immediately(self) -> None:
        self.service.record_stock_in("W001", 5)
        self.assertEqual(self.service.get_product("W001").quantity, 25)

    def test_report_inventory_value_by_category(self) -> None:
        self.service.add_product(
            Product(
                code="M001",
                name="น็อต",
                category=Category(name="ฮาร์ดแวร์"),
                unit_price=2.0,
                quantity=100,
                threshold=20,
            )
        )
        self.service.record_stock_in("W001", 5)

        report = self.service.report_inventory_value_by_category()

        self.assertEqual(report["ไฟฟ้า"], 250.0)
        self.assertEqual(report["ฮาร์ดแวร์"], 200.0)


if __name__ == "__main__":
    unittest.main()
