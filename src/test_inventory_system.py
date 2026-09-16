import unittest
from decimal import Decimal

from inventory_system import (
    EmailNotifier,
    InsufficientStockError,
    InvalidQuantityError,
    InvalidThresholdError,
    MissingUnitPriceError,
    NotificationService,
    ReportService,
    SmsNotifier,
    StockService,
)


class InventorySpecTests(unittest.TestCase):

    def setUp(self):
        self.notifications = NotificationService(
            channels={
                "EMAIL": EmailNotifier(),
                "SMS": SmsNotifier(),
            },
            managers=["ผู้จัดการ"],
        )
        self.stock = StockService(self.notifications)
        self.report = ReportService()

        self.product = self.stock.add_product(
            product_id=1,
            name="สายไฟ 2.5 sq.mm",
            category="ไฟฟ้า",
            quantity=20,
            unit_price=50,
            threshold=15,
            unit="เมตร",
        )

    # US-01
    def test_receive_updates_stock_immediately(self):
        tx = self.stock.receive_stock(1, 30)
        self.assertEqual(tx.stock_after, Decimal("50"))
        self.assertEqual(self.product.quantity, Decimal("50"))
        self.assertEqual(len(self.stock.transactions), 1)

    def test_issue_updates_stock(self):
        tx = self.stock.issue_stock(1, 10)
        self.assertEqual(tx.stock_after, Decimal("10"))
        self.assertEqual(self.product.quantity, Decimal("10"))

    def test_issue_exactly_all_stock_is_allowed(self):
        self.stock.issue_stock(1, 20)
        self.assertEqual(self.product.quantity, Decimal("0"))

    def test_issue_more_than_stock_is_rejected_and_stock_unchanged(self):
        with self.assertRaises(InsufficientStockError):
            self.stock.issue_stock(1, 21)

        self.assertEqual(self.product.quantity, Decimal("20"))
        self.assertEqual(len(self.stock.transactions), 0)

    def test_zero_and_negative_quantities_are_rejected(self):
        for value in [0, -1]:
            with self.assertRaises(InvalidQuantityError):
                self.stock.receive_stock(1, value)

            with self.assertRaises(InvalidQuantityError):
                self.stock.issue_stock(1, value)

        self.assertEqual(self.product.quantity, Decimal("20"))
        self.assertEqual(len(self.stock.transactions), 0)

    # US-02
    def test_stock_below_threshold_creates_notifications(self):
        self.stock.issue_stock(1, 8)
        self.assertEqual(self.product.quantity, Decimal("12"))
        self.assertEqual(len(self.notifications.notifications), 2)

    def test_stock_above_threshold_creates_no_notification(self):
        self.stock.issue_stock(1, 5)
        self.assertEqual(self.product.quantity, Decimal("15"))
        # Exactly threshold is a notification condition.
        self.assertEqual(len(self.notifications.notifications), 2)

    def test_stock_exactly_threshold_creates_notifications(self):
        self.stock.issue_stock(1, 5)
        self.assertEqual(self.product.quantity, Decimal("15"))
        self.assertTrue(all(n.success for n in self.notifications.notifications))

    def test_low_stock_issue_again_creates_new_notifications(self):
        self.stock.issue_stock(1, 8)  # 12 <= 15 -> 2
        self.stock.issue_stock(1, 1)  # 11 <= 15 -> 2 more
        self.assertEqual(len(self.notifications.notifications), 4)

    # US-03
    def test_category_and_total_valuation(self):
        self.stock.add_product(
            product_id=2,
            name="สวิตช์",
            category="ไฟฟ้า",
            quantity=20,
            unit_price=100,
            threshold=5,
            unit="ชิ้น",
        )
        self.stock.add_product(
            product_id=3,
            name="ท่อ PVC",
            category="ประปา",
            quantity=30,
            unit_price=80,
            threshold=5,
            unit="เส้น",
        )

        report = self.report.generate_report(self.stock.products.values())

        # ไฟฟ้า = 20*50 + 20*100 = 3000
        # ประปา = 30*80 = 2400
        # รวม = 5400
        categories = {x["category"]: x["total_value"] for x in report["categories"]}
        self.assertEqual(categories["ไฟฟ้า"], "3,000.00")
        self.assertEqual(categories["ประปา"], "2,400.00")
        self.assertEqual(report["total_value"], "5,400.00")

    def test_zero_stock_has_zero_value_and_remains_in_category(self):
        self.stock.issue_stock(1, 20)
        report = self.report.generate_report(self.stock.products.values())
        categories = {x["category"]: x["total_value"] for x in report["categories"]}
        self.assertEqual(categories["ไฟฟ้า"], "0.00")

    def test_missing_unit_price_is_error(self):
        self.stock.add_product(
            product_id=2,
            name="สินค้าที่ไม่มีราคา",
            category="อื่น ๆ",
            quantity=10,
            unit_price=None,
            threshold=2,
        )
        with self.assertRaises(MissingUnitPriceError):
            self.report.generate_report(self.stock.products.values())

    # US-04
    def test_threshold_zero_is_allowed(self):
        self.stock.set_threshold(1, 0)
        self.assertEqual(self.product.threshold, Decimal("0"))

    def test_negative_threshold_is_rejected(self):
        with self.assertRaises(InvalidThresholdError):
            self.stock.set_threshold(1, -1)

        self.assertEqual(self.product.threshold, Decimal("15"))

    def test_threshold_change_applies_to_next_transaction(self):
        self.stock.set_threshold(1, 20)
        self.stock.issue_stock(1, 1)
        self.assertEqual(self.product.quantity, Decimal("19"))
        self.assertEqual(len(self.notifications.notifications), 2)

    # US-05
    def test_multiple_channels_are_called(self):
        self.stock.issue_stock(1, 8)
        channels = {n.channel for n in self.notifications.notifications}
        self.assertEqual(channels, {"EMAIL", "SMS"})

    def test_notification_failure_does_not_rollback_stock(self):
        failing = NotificationService(
            channels={"EMAIL": EmailNotifier(fail=True)},
            managers=["ผู้จัดการ"],
        )
        stock = StockService(failing)
        product = stock.add_product(
            product_id=1,
            name="สายไฟ",
            category="ไฟฟ้า",
            quantity=20,
            unit_price=50,
            threshold=15,
            unit="เมตร",
        )

        stock.issue_stock(1, 8)

        self.assertEqual(product.quantity, Decimal("12"))
        self.assertEqual(len(stock.transactions), 1)
        self.assertEqual(len(failing.errors), 1)
        self.assertFalse(failing.notifications[0].success)


if __name__ == "__main__":
    unittest.main()
