from typing import Protocol, List, Dict, Type


class Notifier(Protocol):
    """Protocol สำหรับ Observer ที่รับการแจ้งเตือนจาก InventoryService"""

    def send(self, message: str) -> None:
        """ส่งข้อความแจ้งเตือน"""
        ...


class EmailNotifier:
    """ส่งการแจ้งเตือนผ่าน Email (Mock)"""

    def send(self, message: str) -> None:
        print(f"[Email Notifier] {message}")


class SMSNotifier:
    """ส่งการแจ้งเตือนผ่าน SMS (Mock)"""

    def send(self, message: str) -> None:
        print(f"[SMS Notifier] {message}")


class NotifierFactory:
    """Factory Pattern สำหรับสร้าง Notifier Instance จากชื่อช่องทาง"""

    _registry: Dict[str, Type[Notifier]] = {
        "EMAIL": EmailNotifier,
        "SMS": SMSNotifier,
    }

    @classmethod
    def register_notifier(cls, channel_name: str, notifier_cls: Type[Notifier]) -> None:
        """ลงทะเบียนช่องทางการแจ้งเตือนใหม่ (รองรับการขยายโดยไม่ต้องแก้ไขคลาสนี้)"""
        cls._registry[channel_name.upper()] = notifier_cls

    @classmethod
    def create(cls, channel_name: str) -> Notifier:
        """สร้างและคืนค่า Notifier Instance ตามชื่อช่องทางที่กำหนด"""
        key = channel_name.upper()
        if key not in cls._registry:
            raise ValueError(f"ไม่พบช่องทางการแจ้งเตือน: {channel_name}")
        return cls._registry[key]()