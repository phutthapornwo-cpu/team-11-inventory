from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from src.models import Product


class Notifier(Protocol):
    """สัญญาการแจ้งเตือนเมื่อสต็อกต่ำ"""

    def send_low_stock_alert(self, product: Product) -> None:
        """แจ้งเตือนเมื่อสินค้าต่ำกว่า threshold"""


@dataclass
class EmailNotifier:
    """ตัวแจ้งเตือนผ่านอีเมล (จำลองด้วยการพิมพ์ข้อความ)"""

    recipient_email: str

    def send_low_stock_alert(self, product: Product) -> None:
        """ส่งข้อความแจ้งเตือนผ่านอีเมลแบบจำลอง"""
        masked_email = _mask_contact(self.recipient_email)
        print(
            f"[Email] ถึง {masked_email}: สินค้า {product.name} "
            f"({product.code}) คงเหลือ {product.quantity} ต่ำกว่า threshold {product.threshold}"
        )


@dataclass
class SMSNotifier:
    """ตัวแจ้งเตือนผ่าน SMS (จำลองด้วยการพิมพ์ข้อความ)"""

    phone_number: str

    def send_low_stock_alert(self, product: Product) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน SMS แบบจำลอง"""
        masked_phone = _mask_contact(self.phone_number)
        print(
            f"[SMS] ถึง {masked_phone}: สินค้า {product.name} "
            f"({product.code}) คงเหลือ {product.quantity} ต่ำกว่า threshold {product.threshold}"
        )


class NotifierFactory:
    """โรงงานสร้าง notifier ตามช่องทางที่กำหนด"""

    @staticmethod
    def create_notifier(channel: str, target: str) -> Notifier:
        """สร้าง notifier หนึ่งตัวจากชนิดช่องทางและปลายทาง"""
        normalized = channel.lower().strip()
        if normalized == "email":
            return EmailNotifier(recipient_email=target)
        if normalized == "sms":
            return SMSNotifier(phone_number=target)
        raise ValueError(f"ไม่รองรับช่องทางแจ้งเตือน: {channel}")

    @classmethod
    def create_notifiers(cls, configs: list[dict[str, Any]]) -> list[Notifier]:
        """สร้าง notifier หลายตัวจากรายการตั้งค่า"""
        return [
            cls.create_notifier(channel=str(config["channel"]), target=str(config["target"]))
            for config in configs
        ]


def _mask_contact(target: str) -> str:
    if len(target) <= 4:
        return "*" * len(target)
    return f"{target[:2]}{'*' * (len(target) - 4)}{target[-2:]}"
