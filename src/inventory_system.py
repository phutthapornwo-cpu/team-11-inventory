from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from enum import Enum
from time import perf_counter
from typing import Dict, Iterable, List, Optional


# ============================================================
# Domain models
# ============================================================

class TransactionType(str, Enum):
    RECEIVE = "RECEIVE"
    ISSUE = "ISSUE"


@dataclass
class Product:
    id: int
    name: str
    category: str
    quantity: Decimal
    unit_price: Optional[Decimal]
    threshold: Decimal
    unit: str = "หน่วย"


@dataclass
class Transaction:
    transaction_id: int
    product_id: int
    type: TransactionType
    quantity: Decimal
    stock_before: Decimal
    stock_after: Decimal
    timestamp: datetime


@dataclass
class Notification:
    notification_id: int
    product_id: int
    product_name: str
    quantity: Decimal
    threshold: Decimal
    manager: str
    channel: str
    message: str
    timestamp: datetime
    success: bool
    error: Optional[str] = None


@dataclass
class NotificationError:
    product_id: int
    channel: str
    error: str
    timestamp: datetime


# ============================================================
# Exceptions
# ============================================================

class InventoryError(Exception):
    """Base exception for the inventory system."""


class ProductNotFoundError(InventoryError):
    pass


class InvalidQuantityError(InventoryError):
    pass


class InsufficientStockError(InventoryError):
    pass


class InvalidThresholdError(InventoryError):
    pass


class MissingUnitPriceError(InventoryError):
    pass


class DuplicateProductError(InventoryError):
    pass


class NotificationChannelError(Exception):
    """Raised by a notification channel when mock sending fails."""


# ============================================================
# Notification abstraction
# ============================================================

class NotificationChannel(ABC):
    """
    Notification interface.

    Adding a new channel (e.g. LINE) only requires implementing
    this class. StockService does not need to change.
    """

    name: str

    @abstractmethod
    def send(self, manager: str, message: str) -> None:
        raise NotImplementedError


class EmailNotifier(NotificationChannel):
    name = "EMAIL"

    def __init__(self, fail: bool = False):
        self.fail = fail

    def send(self, manager: str, message: str) -> None:
        if self.fail:
            raise NotificationChannelError("Mock Email failed")
        print(f"[MOCK EMAIL] ถึง: {manager}")
        print(message)


class SmsNotifier(NotificationChannel):
    name = "SMS"

    def __init__(self, fail: bool = False):
        self.fail = fail

    def send(self, manager: str, message: str) -> None:
        if self.fail:
            raise NotificationChannelError("Mock SMS failed")
        print(f"[MOCK SMS] ถึง: {manager}")
        print(message)


class NotificationService:
    """
    Handles notifications separately from stock business logic.

    A channel failure must not rollback stock changes.
    """

    def __init__(
        self,
        channels: Optional[Dict[str, NotificationChannel]] = None,
        managers: Optional[Iterable[str]] = None,
    ):
        self.channels: Dict[str, NotificationChannel] = channels or {}
        self.managers: List[str] = list(managers or ["ผู้จัดการ"])
        self.notifications: List[Notification] = []
        self.errors: List[NotificationError] = []
        self._next_notification_id = 1

    def register_channel(self, channel: NotificationChannel) -> None:
        self.channels[channel.name] = channel

    def set_managers(self, managers: Iterable[str]) -> None:
        self.managers = list(managers)

    @staticmethod
    def build_low_stock_message(product: Product) -> str:
        return (
            f"สินค้า: {product.name}\n"
            f"สต็อกคงเหลือ: {format_decimal(product.quantity)} {product.unit}\n"
            f"Threshold: {format_decimal(product.threshold)} {product.unit}\n"
            f"ประเภท: LOW_STOCK"
        )

    def notify_low_stock(self, product: Product) -> None:
        """
        Send to every configured manager through every selected channel.

        Notification is mock-only: Email/SMS print to console.
        Channel failures are recorded and do not affect stock.
        """
        message = self.build_low_stock_message(product)
        timestamp = now_utc()

        for manager in self.managers:
            for channel_name, channel in self.channels.items():
                success = True
                error_text = None

                try:
                    channel.send(manager, message)
                except Exception as exc:
                    success = False
                    error_text = str(exc)
                    self.errors.append(
                        NotificationError(
                            product_id=product.id,
                            channel=channel_name,
                            error=error_text,
                            timestamp=timestamp,
                        )
                    )
                    print(
                        f"[NOTIFICATION ERROR] channel={channel_name}, "
                        f"product={product.name}, error={error_text}"
                    )

                self.notifications.append(
                    Notification(
                        notification_id=self._next_notification_id,
                        product_id=product.id,
                        product_name=product.name,
                        quantity=product.quantity,
                        threshold=product.threshold,
                        manager=manager,
                        channel=channel_name,
                        message=message,
                        timestamp=timestamp,
                        success=success,
                        error=error_text,
                    )
                )
                self._next_notification_id += 1


# ============================================================
# Stock service
# ============================================================

class StockService:
    """
    Owns stock business rules.

    Rules:
      - quantity must be > 0 for receive/issue
      - issue quantity must not exceed current stock
      - stock can become exactly 0
      - rejected transactions do not change stock
      - issue resulting in quantity <= threshold triggers notification
    """

    def __init__(self, notification_service: NotificationService):
        self.products: Dict[int, Product] = {}
        self.transactions: List[Transaction] = []
        self.notification_service = notification_service
        self._next_transaction_id = 1

    def add_product(
        self,
        product_id: int,
        name: str,
        category: str,
        quantity: object,
        unit_price: Optional[object],
        threshold: object,
        unit: str = "หน่วย",
    ) -> Product:
        if product_id in self.products:
            raise DuplicateProductError(f"Product id {product_id} already exists")

        qty = to_decimal(quantity, "quantity")
        price = None if unit_price is None else to_decimal(unit_price, "unitPrice")
        th = to_decimal(threshold, "threshold")

        if qty < 0:
            raise InvalidQuantityError("Initial quantity must be >= 0")
        validate_threshold(th)

        product = Product(
            id=product_id,
            name=name,
            category=category,
            quantity=qty,
            unit_price=price,
            threshold=th,
            unit=unit,
        )
        self.products[product_id] = product
        return product

    def get_product(self, product_id: int) -> Product:
        try:
            return self.products[product_id]
        except KeyError:
            raise ProductNotFoundError(f"Product {product_id} not found")

    def receive_stock(self, product_id: int, quantity: object) -> Transaction:
        amount = validate_transaction_quantity(quantity)
        product = self.get_product(product_id)

        stock_before = product.quantity
        stock_after = stock_before + amount

        # Update only after all validation has passed.
        product.quantity = stock_after
        transaction = self._record_transaction(
            product=product,
            transaction_type=TransactionType.RECEIVE,
            quantity=amount,
            stock_before=stock_before,
            stock_after=stock_after,
        )
        return transaction

    def issue_stock(self, product_id: int, quantity: object) -> Transaction:
        amount = validate_transaction_quantity(quantity)
        product = self.get_product(product_id)

        if amount > product.quantity:
            raise InsufficientStockError(
                f"สต็อกไม่เพียงพอ: มี {format_decimal(product.quantity)} "
                f"{product.unit} แต่ต้องการจ่าย {format_decimal(amount)} {product.unit}"
            )

        stock_before = product.quantity
        stock_after = stock_before - amount

        # Stock update and transaction are completed before notification.
        # Notification failure therefore cannot rollback stock.
        product.quantity = stock_after
        transaction = self._record_transaction(
            product=product,
            transaction_type=TransactionType.ISSUE,
            quantity=amount,
            stock_before=stock_before,
            stock_after=stock_after,
        )

        # FR-06/FR-07: only ISSUE is a low-stock trigger.
        # quantity <= threshold includes equality.
        if product.quantity <= product.threshold:
            self.notification_service.notify_low_stock(product)

        return transaction

    def set_threshold(self, product_id: int, threshold: object) -> Decimal:
        new_threshold = to_decimal(threshold, "threshold")
        validate_threshold(new_threshold)

        product = self.get_product(product_id)
        product.threshold = new_threshold
        return new_threshold

    def _record_transaction(
        self,
        product: Product,
        transaction_type: TransactionType,
        quantity: Decimal,
        stock_before: Decimal,
        stock_after: Decimal,
    ) -> Transaction:
        transaction = Transaction(
            transaction_id=self._next_transaction_id,
            product_id=product.id,
            type=transaction_type,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=stock_after,
            timestamp=now_utc(),
        )
        self.transactions.append(transaction)
        self._next_transaction_id += 1
        return transaction


# ============================================================
# Report service
# ============================================================

class ReportService:
    """
    Calculates inventory valuation.

    Formula:
        product_value = quantity * unit_price
        category_value = sum(product_value)
        total_value = sum(category_value)
    """

    MONEY_QUANT = Decimal("0.01")

    @classmethod
    def calculate_product_value(cls, product: Product) -> Decimal:
        if product.unit_price is None:
            raise MissingUnitPriceError(
                f"สินค้า '{product.name}' ไม่มีราคาต้นทุน (unitPrice)"
            )

        value = product.quantity * product.unit_price
        return value.quantize(cls.MONEY_QUANT, rounding=ROUND_HALF_UP)

    @classmethod
    def calculate_category_values(
        cls, products: Iterable[Product]
    ) -> Dict[str, Decimal]:
        result: Dict[str, Decimal] = {}

        for product in products:
            value = cls.calculate_product_value(product)
            result[product.category] = (
                result.get(product.category, Decimal("0")) + value
            )

        return {
            category: value.quantize(cls.MONEY_QUANT, rounding=ROUND_HALF_UP)
            for category, value in result.items()
        }

    @classmethod
    def calculate_total_value(cls, products: Iterable[Product]) -> Decimal:
        total = sum(
            (cls.calculate_product_value(product) for product in products),
            Decimal("0"),
        )
        return total.quantize(cls.MONEY_QUANT, rounding=ROUND_HALF_UP)

    @classmethod
    def generate_report(cls, products: Iterable[Product]) -> dict:
        products = list(products)
        category_values = cls.calculate_category_values(products)
        total = cls.calculate_total_value(products)

        return {
            "categories": [
                {
                    "category": category,
                    "total_value": format_decimal(value, money=True),
                }
                for category, value in sorted(category_values.items())
            ],
            "total_value": format_decimal(total, money=True),
        }

    @classmethod
    def benchmark(cls, products: Iterable[Product]) -> float:
        """
        Benchmark only the Report Service processing time.
        UI rendering is intentionally excluded.
        """
        products = list(products)
        start = perf_counter()
        cls.generate_report(products)
        return perf_counter() - start


# ============================================================
# Helpers
# ============================================================

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_decimal(value: object, field_name: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{field_name} ต้องเป็นตัวเลข")

    if not result.is_finite():
        raise ValueError(f"{field_name} ต้องเป็นตัวเลขที่มีค่าจำกัด")

    return result


def validate_transaction_quantity(value: object) -> Decimal:
    quantity = to_decimal(value, "quantity")
    if quantity <= 0:
        raise InvalidQuantityError("จำนวนรับ/จ่ายต้องมากกว่า 0")
    return quantity


def validate_threshold(threshold: Decimal) -> None:
    if threshold < 0:
        raise InvalidThresholdError(
            "Threshold ต้องมากกว่าหรือเท่ากับ 0"
        )


def format_decimal(value: Decimal, money: bool = False) -> str:
    if money:
        value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{value:,.2f}"
    return format(value, "f")


# ============================================================
# Demo
# ============================================================

def create_demo_system() -> tuple[StockService, NotificationService, ReportService]:
    notification_service = NotificationService(
        channels={
            "EMAIL": EmailNotifier(),
            "SMS": SmsNotifier(),
        },
        managers=["ผู้จัดการ"],
    )

    stock_service = StockService(notification_service)
    report_service = ReportService()

    stock_service.add_product(
        product_id=1,
        name="สายไฟ 2.5 sq.mm",
        category="ไฟฟ้า",
        quantity=20,
        unit_price=50,
        threshold=15,
        unit="เมตร",
    )

    stock_service.add_product(
        product_id=2,
        name="สวิตช์ไฟ",
        category="ไฟฟ้า",
        quantity=20,
        unit_price=100,
        threshold=5,
        unit="ชิ้น",
    )

    stock_service.add_product(
        product_id=3,
        name="ท่อ PVC",
        category="ประปา",
        quantity=30,
        unit_price=80,
        threshold=5,
        unit="เส้น",
    )

    return stock_service, notification_service, report_service


def print_report(stock_service: StockService, report_service: ReportService) -> None:
    report = report_service.generate_report(stock_service.products.values())

    print("\n===== STOCK VALUATION REPORT =====")
    for row in report["categories"]:
        print(f"{row['category']}: {row['total_value']} บาท")
    print(f"รวมทั้งหมด: {report['total_value']} บาท")


def demo() -> None:
    stock_service, notification_service, report_service = create_demo_system()

    print("===== RECEIVE =====")
    tx = stock_service.receive_stock(1, 30)
    print(
        f"รับสำเร็จ: transaction={tx.transaction_id}, "
        f"stock={format_decimal(tx.stock_after)} เมตร"
    )

    print("\n===== ISSUE ABOVE THRESHOLD =====")
    tx = stock_service.issue_stock(1, 20)
    print(
        f"จ่ายสำเร็จ: transaction={tx.transaction_id}, "
        f"stock={format_decimal(tx.stock_after)} เมตร"
    )

    print("\n===== ISSUE TO THRESHOLD =====")
    # Current stock = 30, threshold = 15
    # Issue 15 -> exactly threshold -> EMAIL + SMS mock notification.
    tx = stock_service.issue_stock(1, 15)
    print(
        f"จ่ายสำเร็จ: transaction={tx.transaction_id}, "
        f"stock={format_decimal(tx.stock_after)} เมตร"
    )

    print("\n===== ISSUE WHILE ALREADY LOW =====")
    # Stock is already 15 <= threshold 15.
    # Every issue transaction while the resulting stock is <= threshold
    # creates a new notification.
    tx = stock_service.issue_stock(1, 1.5)
    print(
        f"จ่ายสำเร็จ: transaction={tx.transaction_id}, "
        f"stock={format_decimal(tx.stock_after)} เมตร"
    )

    print_report(stock_service, report_service)

    print("\n===== NOTIFICATION SUMMARY =====")
    print(f"notifications: {len(notification_service.notifications)}")
    print(f"errors: {len(notification_service.errors)}")


if __name__ == "__main__":
    demo()
