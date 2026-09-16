# Inventory Management - Spec-Driven Python Implementation

ไฟล์นี้เป็น implementation ตาม `inventory_spec_revised.md` โดยใช้ Python Standard Library เท่านั้น
และเก็บข้อมูลทั้งหมดใน Memory

## ไฟล์

- `inventory_system.py` — ระบบหลัก
- `test_inventory_system.py` — Automated tests สำหรับ Acceptance Criteria สำคัญ

## วิธีรัน

```bash
python inventory_system.py
```

ระบบ Demo จะสาธิต:
- รับสินค้า
- จ่ายสินค้า
- จ่ายแล้วมากกว่า threshold
- จ่ายจนเท่ากับ threshold
- จ่ายซ้ำขณะที่ stock ต่ำ
- Notification แบบ Mock Email/SMS
- รายงานมูลค่าสต็อก

## รัน Test

```bash
python -m unittest -v test_inventory_system.py
```

## โครงสร้าง

```text
StockService
├── receive_stock()
├── issue_stock()
├── set_threshold()
└── transactions (Memory)

NotificationService
├── EmailNotifier
├── SmsNotifier
└── errors / notifications (Memory)

ReportService
├── calculate_product_value()
├── calculate_category_values()
├── calculate_total_value()
└── generate_report()
```

## Business Rules ที่ implementation ใช้

### Quantity

```text
receiveQuantity > 0
issueQuantity > 0
issueQuantity <= currentQuantity
```

จ่ายเท่ากับ stock ได้ และ stock สามารถเป็น 0 ได้

### Low Stock

```text
quantity <= threshold
    -> สร้าง Notification
quantity > threshold
    -> ไม่สร้าง Notification
```

Notification ถูก trigger จาก `ISSUE` transaction ตาม FR-06/FR-07

ทุก issue transaction ที่ทำให้ stock หลังจ่ายยัง `<= threshold`
จะสร้าง notification ใหม่ตาม spec

### Threshold

```text
threshold >= 0
```

ดังนั้น `threshold = 0` ใช้ได้ แต่ค่าติดลบใช้ไม่ได้

### Stock Valuation

```text
productValue = quantity * unitPrice
categoryValue = sum(productValue)
totalValue = sum(categoryValue)
```

`unitPrice` คือราคาต้นทุนต่อหน่วย และแสดงเงินด้วยทศนิยม 2 ตำแหน่ง

หากสินค้าไม่มี `unitPrice` ระบบจะ raise `MissingUnitPriceError`
แทนการถือว่ามูลค่าเป็น 0 โดยอัตโนมัติ

## Notification Failure

Notification ถูกแยกจาก Stock Business Logic

ลำดับของการจ่าย:

```text
ตรวจสอบ quantity
      ↓
อัปเดต stock
      ↓
บันทึก transaction
      ↓
ตรวจ quantity <= threshold
      ↓
สร้าง notification
```

ถ้า Email/SMS Mock ล้มเหลว:

```text
Stock update = สำเร็จ
Transaction = สำเร็จ
Notification = failure ถูกบันทึกใน errors
```

ไม่มี rollback stock

## เพิ่มช่องทางใหม่

สามารถเพิ่ม `LineNotifier` หรือช่องทางอื่นโดย implement:

```python
class LineNotifier(NotificationChannel):
    name = "LINE"

    def send(self, manager: str, message: str) -> None:
        print(f"[MOCK LINE] ถึง: {manager}")
        print(message)
```

จากนั้น register:

```python
notification_service.register_channel(LineNotifier())
```

โดยไม่ต้องแก้ `StockService`
