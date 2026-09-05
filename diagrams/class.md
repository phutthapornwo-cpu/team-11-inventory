# Class Diagram

แผนภาพนี้สรุปโครงสร้างคลาสจาก `src/models.py`, `src/notifiers.py`, และ `src/service.py` โดยแสดงแอตทริบิวต์ เมธอด visibility และความสัมพันธ์หลัก ได้แก่ realization, composition และ dependency

```mermaid
classDiagram
    class Category {
        +name: str
    }

    class Product {
        +code: str
        +name: str
        +category: Category
        +unit_price: float
        +quantity: int
        +threshold: int
        +__post_init__() None
        +increase_stock(quantity: int) None
        +decrease_stock(quantity: int) None
        +is_low_stock() bool
        +inventory_value() float
    }

    class StockTransaction {
        +product_code: str
        +quantity: int
        +transaction_type: Literal["IN","OUT"]
    }

    class Notifier {
        <<Protocol>>
        +send_low_stock_alert(product: Product) None
    }

    class EmailNotifier {
        +recipient_email: str
        +send_low_stock_alert(product: Product) None
    }

    class SMSNotifier {
        +phone_number: str
        +send_low_stock_alert(product: Product) None
    }

    class NotifierFactory {
        +create_notifier(channel: str, target: str) Notifier
        +create_notifiers(configs: list[dict[str, Any]]) list[Notifier]
    }

    class InventoryService {
        -_notifiers: list[Notifier]
        -_products: dict[str, Product]
        +add_product(product: Product) None
        +record_stock_in(product_code: str, quantity: int) StockTransaction
        +record_stock_out(product_code: str, quantity: int) StockTransaction
        +get_product(product_code: str) Product
        +report_inventory_value_by_category() dict[str, float]
        -_get_product_or_raise(product_code: str) Product
    }

    Product *-- Category : composition
    InventoryService *-- Product : composition
    InventoryService ..> StockTransaction : dependency
    InventoryService ..> Notifier : dependency
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization
    NotifierFactory ..> Notifier : dependency
    NotifierFactory ..> EmailNotifier : dependency
    NotifierFactory ..> SMSNotifier : dependency
    EmailNotifier ..> Product : dependency
    SMSNotifier ..> Product : dependency
```

คำอธิบายความสัมพันธ์:
- `Product` มี `Category` เป็นส่วนประกอบของข้อมูลสินค้า
- `InventoryService` ครอบครองรายการสินค้าและรายการ notifier ที่ใช้งานจริง
- `InventoryService` พึ่งพา `Notifier` เพื่อแจ้งเตือน และพึ่งพา `StockTransaction` เป็นผลลัพธ์ของการทำรายการรับ/จ่าย
- `EmailNotifier` และ `SMSNotifier` ทำตามสัญญา `Notifier` (realization)
- `NotifierFactory` พึ่งพาคลาส notifier ที่สร้างออกมา
