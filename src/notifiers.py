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
        print(
            f"[Email] ถึง {self.recipient_email}: สินค้า {product.name} "
            f"({product.code}) คงเหลือ {product.quantity} ต่ำกว่า threshold {product.threshold}"
        )


@dataclass
class SMSNotifier:
    """ตัวแจ้งเตือนผ่าน SMS (จำลองด้วยการพิมพ์ข้อความ)"""

    phone_number: str

    def send_low_stock_alert(self, product: Product) -> None:
        """ส่งข้อความแจ้งเตือนผ่าน SMS แบบจำลอง"""
        print(
            f"[SMS] ถึง {self.phone_number}: สินค้า {product.name} "
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
