# Spec: ฟีเจอร์แจ้งเตือนสต็อกต่ำ และรายงานมูลค่าสต็อก

## 1. เป้าหมาย (Goal)

เพิ่มความสามารถให้ระบบ Inventory แจ้งเตือนผู้จัดการเมื่อสินค้าใดมีสต็อกคงเหลือน้อยกว่าหรือเท่ากับ threshold และให้ผู้จัดการดูรายงานมูลค่าสต็อกแยกตามหมวดหมู่ได้

---

## 2. User Story

| รหัส | User Story |
|---|---|
| US-01 | As a พนักงานคลังสินค้า, I want บันทึกการรับ/จ่ายสินค้าพร้อมอัปเดตสต็อกทันที, so that สต็อกในระบบสะท้อนจำนวนจริง |
| US-02 | As a ผู้จัดการ, I want รับการแจ้งเตือนเมื่อสินค้าใดมีสต็อกคงเหลือน้อยกว่าหรือเท่ากับ threshold, so that สั่งซื้อได้ก่อนของหมด |
| US-03 | As a ผู้จัดการ, I want ดูมูลค่ารวมของสต็อกแยกตามหมวดหมู่, so that ตัดสินใจด้านการเงินได้ |
| US-04 | As a ผู้จัดการ, I want ตั้งค่า threshold ของสินค้าแต่ละรายการ, so that ระบบสามารถแจ้งเตือนเมื่อสินค้าเหลือถึงระดับที่กำหนด |
| US-05 | As a ผู้จัดการ, I want เลือกช่องทางการแจ้งเตือน เช่น Email หรือ SMS, so that สามารถกำหนดช่องทางที่ต้องการรับการแจ้งเตือนได้ |

---

## 3. Acceptance Criteria (Given-When-Then)

### AC ของ US-01

#### Scenario: รับสินค้าเข้าสต็อก

```gherkin
Scenario: รับสินค้าเข้าสต็อก
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 20 เมตร
  When พนักงานบันทึกรับสินค้า 30 เมตร
  Then สต็อกคงเหลือ 50 เมตร
  And ระบบบันทึก transaction การรับสินค้า
```

#### Scenario: จ่ายสินค้าโดยมีสต็อกเพียงพอ

```gherkin
Scenario: จ่ายสินค้าโดยมีสต็อกเพียงพอ
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 50 เมตร
  When พนักงานบันทึกจ่ายออก 10 เมตร
  Then สต็อกคงเหลือ 40 เมตร
  And ระบบบันทึก transaction การจ่ายสินค้า
```

#### Scenario: จ่ายสินค้าจนหมดพอดี

```gherkin
Scenario: จ่ายสินค้าจนหมดพอดี
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 10 เมตร
  When พนักงานบันทึกจ่ายออก 10 เมตร
  Then ระบบยอมรับรายการ
  And สต็อกคงเหลือ 0 เมตร
  And ระบบบันทึก transaction การจ่ายสินค้า
```

#### Scenario: จ่ายสินค้าเกินจำนวนที่มี

```gherkin
Scenario: จ่ายสินค้าเกินจำนวนที่มี
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 5 เมตร
  When พนักงานบันทึกจ่ายออก 10 เมตร
  Then ระบบปฏิเสธรายการ
  And สต็อกคงเหลือยังเป็น 5 เมตร
  And ระบบแสดงข้อความ "สต็อกไม่เพียงพอ"
```

#### Scenario: รับสินค้าด้วยจำนวนไม่ถูกต้อง

```gherkin
Scenario: รับสินค้าด้วยจำนวนศูนย์หรือติดลบ
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 20 เมตร
  When พนักงานบันทึกรับสินค้า 0 เมตรหรือจำนวนติดลบ
  Then ระบบปฏิเสธรายการ
  And สต็อกคงเหลือยังเป็น 20 เมตร
```

#### Scenario: จ่ายสินค้าด้วยจำนวนศูนย์หรือติดลบ

```gherkin
Scenario: จ่ายสินค้าด้วยจำนวนศูนย์หรือติดลบ
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 20 เมตร
  When พนักงานบันทึกจ่ายสินค้า 0 เมตรหรือจำนวนติดลบ
  Then ระบบปฏิเสธรายการ
  And สต็อกคงเหลือยังเป็น 20 เมตร
```

### AC ของ US-02

> กฎการแจ้งเตือน: ระบบต้องแจ้งเตือนเมื่อ `quantity <= threshold`

#### Scenario: จ่ายสินค้าจนสต็อกต่ำกว่า threshold

```gherkin
Scenario: จ่ายสินค้าจนสต็อกต่ำกว่า threshold
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 20 เมตร และ threshold = 15
  When พนักงานบันทึกจ่ายออก 8 เมตร
  Then สต็อกคงเหลือ 12 เมตร
  And ระบบสร้างการแจ้งเตือนถึงผู้จัดการภายใน 1 วินาทีหลังอัปเดตสต็อก
```

#### Scenario: จ่ายสินค้าโดยสต็อกยังสูงกว่า threshold

```gherkin
Scenario: จ่ายสินค้าโดยสต็อกยังสูงกว่า threshold
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 50 เมตร และ threshold = 15
  When พนักงานบันทึกจ่ายออก 10 เมตร
  Then สต็อกคงเหลือ 40 เมตร
  And ระบบไม่สร้างการแจ้งเตือน
```

#### Scenario: สต็อกคงเหลือเท่ากับ threshold

```gherkin
Scenario: สต็อกคงเหลือเท่ากับ threshold
  Given สินค้า "สายไฟ 2.5 sq.mm" มีสต็อก 20 เมตร และ threshold = 15
  When พนักงานบันทึกจ่ายออก 5 เมตร
  Then สต็อกคงเหลือ 15 เมตร
  And ระบบสร้างการแจ้งเตือนถึงผู้จัดการภายใน 1 วินาทีหลังอัปเดตสต็อก
```

#### Scenario: สต็อกยังต่ำกว่า threshold และมีการจ่ายซ้ำ

```gherkin
Scenario: สต็อกยังต่ำกว่า threshold และมีการจ่ายซ้ำ
  Given สินค้ามีสต็อก 8 หน่วย และ threshold = 10
  When พนักงานบันทึกจ่ายออก 1 หน่วย
  Then สต็อกคงเหลือ 7 หน่วย
  And ระบบสร้างการแจ้งเตือนสำหรับ transaction นี้
```

> หมายเหตุ: ระบบถือว่าแต่ละ transaction ที่ทำให้ `quantity <= threshold` เป็นเหตุให้สร้างการแจ้งเตือนใหม่ เพื่อให้พฤติกรรม deterministic และทดสอบได้

### AC ของ US-03

#### Scenario: คำนวณมูลค่าสต็อกของหมวดหมู่

```gherkin
Scenario: คำนวณมูลค่าสต็อกของหมวดหมู่
  Given หมวดหมู่ "ไฟฟ้า" มีสินค้า
    | สินค้า | จำนวน | ราคาต่อหน่วย |
    | สายไฟ | 100 | 50 |
    | สวิตช์ | 20 | 100 |
  When ผู้จัดการเปิดรายงานมูลค่าสต็อก
  Then ระบบแสดงมูลค่าหมวด "ไฟฟ้า" เท่ากับ 7,000 บาท
```

> สูตร: `มูลค่าสต็อก = quantity × unitPrice` โดย `unitPrice` หมายถึงราคาต้นทุนต่อหน่วย และระบบใช้ทศนิยม 2 ตำแหน่งในการแสดงผล

#### Scenario: แสดงมูลค่าสต็อกแยกตามหมวดหมู่

```gherkin
Scenario: แสดงมูลค่าสต็อกแยกตามหมวดหมู่
  Given มีสินค้าในหมวด "ไฟฟ้า" และ "ประปา"
  When ผู้จัดการเปิดรายงานมูลค่าสต็อก
  Then ระบบแสดงชื่อหมวดหมู่
  And ระบบแสดงมูลค่าสต็อกของแต่ละหมวดหมู่แยกจากกัน
  And ระบบแสดงมูลค่าสต็อกรวมทั้งหมด
```

#### Scenario: สินค้าที่มีสต็อกเป็นศูนย์

```gherkin
Scenario: แสดงสินค้าที่มีสต็อกเป็นศูนย์
  Given มีสินค้า "สวิตช์" ในหมวด "ไฟฟ้า" และมีสต็อก 0 ชิ้น
  When ผู้จัดการเปิดรายงานมูลค่าสต็อก
  Then ระบบคำนวณมูลค่าของสินค้านั้นเป็น 0 บาท
  And ระบบยังคงรวมสินค้าในรายงานของหมวด "ไฟฟ้า"
```

#### Scenario: รายการสินค้าที่มีราคาต้นทุนไม่ครบ

```gherkin
Scenario: สินค้าไม่มีราคาต้นทุน
  Given มีสินค้าที่มี quantity แต่ไม่มี unitPrice
  When ผู้จัดการเปิดรายงานมูลค่าสต็อก
  Then ระบบไม่คำนวณรายการนั้นเป็นมูลค่า 0 โดยอัตโนมัติ
  And ระบบแสดงข้อผิดพลาดว่าราคาต้นทุนไม่ครบ
```

### AC ของ US-04

#### Scenario: ผู้จัดการกำหนด threshold ของสินค้า

```gherkin
Scenario: ผู้จัดการกำหนด threshold ของสินค้า
  Given สินค้า "สายไฟ 2.5 sq.mm" มี threshold = 15
  When ผู้จัดการเปลี่ยน threshold เป็น 20
  Then ระบบบันทึก threshold ใหม่เป็น 20
  And threshold ใหม่มีผลทันทีสำหรับ transaction ถัดไป
```

#### Scenario: ผู้จัดการกำหนด threshold เป็นศูนย์

```gherkin
Scenario: ผู้จัดการกำหนด threshold เป็นศูนย์
  Given ผู้จัดการกำลังตั้งค่า threshold
  When ผู้จัดการกำหนด threshold เป็น 0
  Then ระบบยอมรับค่า threshold
  And ระบบใช้ค่า 0 ในการตรวจสอบสต็อก
```

#### Scenario: ผู้จัดการกำหนด threshold เป็นค่าติดลบ

```gherkin
Scenario: ผู้จัดการกำหนด threshold เป็นค่าติดลบ
  Given ผู้จัดการกำลังตั้งค่า threshold
  When ผู้จัดการกำหนด threshold เป็น -5
  Then ระบบปฏิเสธข้อมูล
  And ระบบแสดงข้อความ "Threshold ต้องมากกว่าหรือเท่ากับ 0"
```

### AC ของ US-05

#### Scenario: เลือกช่องทางแจ้งเตือน Email

```gherkin
Scenario: เลือกช่องทางแจ้งเตือน Email
  Given ผู้จัดการเลือกช่องทางการแจ้งเตือนเป็น Email
  When สินค้ามีสต็อกต่ำกว่าหรือเท่ากับ threshold
  Then ระบบเรียกใช้ Email Notifier
  And ระบบแสดงข้อความจำลองการส่ง Email
```

#### Scenario: เลือกช่องทางแจ้งเตือน SMS

```gherkin
Scenario: เลือกช่องทางแจ้งเตือน SMS
  Given ผู้จัดการเลือกช่องทางการแจ้งเตือนเป็น SMS
  When สินค้ามีสต็อกต่ำกว่าหรือเท่ากับ threshold
  Then ระบบเรียกใช้ SMS Notifier
  And ระบบแสดงข้อความจำลองการส่ง SMS
```

#### Scenario: เลือกหลายช่องทางพร้อมกัน

```gherkin
Scenario: เลือกหลายช่องทางแจ้งเตือน
  Given ผู้จัดการเลือกช่องทาง Email และ SMS
  When สินค้ามีสต็อกต่ำกว่าหรือเท่ากับ threshold
  Then ระบบเรียกใช้ Email Notifier
  And ระบบเรียกใช้ SMS Notifier
```

---

## 4. In Scope / Out of Scope

### In Scope

- บันทึกการรับสินค้า
- บันทึกการจ่ายสินค้า
- อัปเดตสต็อกทันที
- ตรวจสอบจำนวนสินค้าก่อนจ่าย
- ป้องกันสต็อกติดลบ
- ตั้งค่า threshold รายสินค้า
- ตรวจสอบสต็อกกับ threshold
- แจ้งเตือนเมื่อ `quantity <= threshold`
- รองรับการแจ้งเตือน Email และ SMS แบบจำลอง
- แสดงรายงานมูลค่าสต็อก
- แสดงมูลค่าสต็อกแยกตามหมวดหมู่
- แสดงมูลค่าสต็อกรวม
- เก็บข้อมูลสต็อกใน Memory
- บันทึก transaction ใน Memory

### Out of Scope

- การส่ง Email จริง
- การส่ง SMS จริง
- ระบบ Login
- ระบบกำหนดสิทธิ์ผู้ใช้งาน
- ฐานข้อมูลถาวร
- การเชื่อมต่อระบบจัดซื้อ
- การเชื่อมต่อระบบชำระเงิน

**ฐานข้อมูลถาวร:** ไม่ทำในขอบเขตของงานนี้ โดยระบบจะเก็บข้อมูลไว้ใน Memory เท่านั้น

---

## 5. Functional Requirements (FR)

| รหัส | ความต้องการ | จาก Story |
|---|---|---|
| FR-01 | ระบบต้องอัปเดตสต็อกทันทีหลังบันทึกรับ/จ่ายที่ผ่านการตรวจสอบ | US-01 |
| FR-02 | ระบบต้องตรวจสต็อกก่อนจ่าย และปฏิเสธถ้าสต็อกไม่เพียงพอ | US-01 |
| FR-03 | ระบบต้องไม่อนุญาตให้จำนวนสต็อกติดลบ | US-01 |
| FR-04 | ระบบต้องบันทึก transaction การรับและจ่ายสินค้าที่สำเร็จ | US-01 |
| FR-05 | ระบบต้องปฏิเสธ quantity ที่น้อยกว่าหรือเท่ากับ 0 | US-01 |
| FR-06 | ระบบต้องแจ้งเตือนเมื่อสต็อกหลังจ่ายน้อยกว่าหรือเท่ากับ threshold | US-02 |
| FR-07 | ระบบต้องไม่สร้างการแจ้งเตือนเมื่อสต็อกหลังจ่ายมากกว่า threshold | US-02 |
| FR-08 | ระบบต้องสร้างการแจ้งเตือนใหม่สำหรับทุก transaction ที่ทำให้เกิดเงื่อนไข `quantity <= threshold` | US-02 |
| FR-09 | ระบบต้องคำนวณมูลค่าสต็อกจาก `quantity × unitPrice` โดย `unitPrice` คือราคาต้นทุนต่อหน่วย | US-03 |
| FR-10 | ระบบต้องรวมและแสดงมูลค่าสต็อกแยกตามหมวดหมู่ และแสดงมูลค่ารวมทั้งหมด | US-03 |
| FR-11 | ระบบต้องให้ผู้จัดการกำหนด threshold ของสินค้าแต่ละรายการ | US-04 |
| FR-12 | ระบบต้องยอมรับ threshold ที่มีค่า 0 และปฏิเสธค่าติดลบ | US-04 |
| FR-13 | ระบบต้องรองรับช่องทางแจ้งเตือน Email และ SMS | US-05 |
| FR-14 | ระบบต้องรองรับการเลือกช่องทางแจ้งเตือนมากกว่าหนึ่งช่องทาง | US-05 |
| FR-15 | ระบบต้องแยก Notification Logic ออกจาก Stock Business Logic | US-02, US-05 |

---

## 6. Non-Functional Requirements (NFR)

| รหัส | มิติ | ความต้องการ (ต้องวัดได้) |
|---|---|---|
| NFR-01 | Performance | รายงานมูลค่าสต็อก 1,000 รายการต้องประมวลผลเสร็จภายใน 1 วินาที โดยวัดที่การประมวลผลของ Report Service ไม่รวมเวลาการแสดงผล UI |
| NFR-02 | Maintainability | การเพิ่มช่องทางแจ้งเตือนใหม่ต้องไม่ต้องแก้ไข Stock Business Logic |
| NFR-03 | Reliability | หาก Notification Channel ใดล้มเหลว การอัปเดตสต็อกและ transaction ที่สำเร็จแล้วต้องไม่ถูกยกเลิก |
| NFR-04 | Performance | การรับหรือจ่ายสินค้า 1 รายการต้องประมวลผลเสร็จภายใน 500 ms โดยวัดจาก Service Layer และไม่รวมเวลาการแสดงผล UI |
| NFR-05 | Maintainability | Stock Logic, Notification Logic และ Report Logic ต้องแยกเป็นส่วนที่มีหน้าที่ชัดเจนและทดสอบแยกกันได้ |
| NFR-06 | Scalability | ระบบต้องสามารถเพิ่มช่องทางแจ้งเตือน เช่น LINE ได้โดยไม่ต้องแก้ Stock Service |
| NFR-07 | Data Integrity | Transaction ที่ถูกปฏิเสธต้องไม่เปลี่ยนแปลงจำนวน stock และต้องไม่ถูกบันทึกเป็น transaction สำเร็จ |

---

## 7. Design Notes

- การแจ้งเตือนต้องแยกออกจาก Business Logic ของ Stock
- ระบบต้องรองรับหลายช่องทางการแจ้งเตือน
- ควรออกแบบ Notification แบบ Interface/Strategy เพื่อให้เพิ่มช่องทางใหม่ได้ง่าย
- Stock Service มีหน้าที่จัดการจำนวนสินค้าเท่านั้น
- Notification Service มีหน้าที่จัดการการแจ้งเตือน
- Report Service มีหน้าที่คำนวณและสรุปมูลค่าสต็อก
- ระบบใช้ Memory เป็นที่เก็บข้อมูลชั่วคราว
- เมื่อโปรแกรมหยุดทำงาน ข้อมูลใน Memory จะหายไป
- การคำนวณมูลค่าใช้ `quantity × unitPrice`
- `unitPrice` หมายถึงราคาต้นทุนต่อหน่วย
- แสดงมูลค่าด้วยทศนิยม 2 ตำแหน่ง
- การแจ้งเตือนเกิดขึ้นเมื่อ `quantity <= threshold`
- หาก transaction ทำให้ stock เข้าเงื่อนไข `quantity <= threshold` ให้สร้าง notification event ใหม่สำหรับ transaction นั้น
- หาก notification channel ล้มเหลว ต้องไม่ rollback การเปลี่ยนแปลง stock
- Notification แบบ Email/SMS เป็น Mock โดยใช้การพิมพ์ข้อความแทนการส่งจริง

### รูปแบบข้อความแจ้งเตือนขั้นต่ำ

```text
สินค้า: สายไฟ 2.5 sq.mm
สต็อกคงเหลือ: 12 เมตร
Threshold: 15 เมตร
ประเภท: LOW_STOCK
```

---

## 8. โครงสร้างข้อมูล

ตัวอย่าง Product:

```text
Product
├── id
├── name
├── category
├── quantity
├── unitPrice
└── threshold
```

ตัวอย่าง Transaction:

```text
Transaction
├── transactionId
├── productId
├── type
├── quantity
├── stockBefore
├── stockAfter
└── timestamp
```

โดย `type` ต้องเป็นหนึ่งใน:

```text
RECEIVE
ISSUE
```

ตัวอย่าง Product:

```json
{
  "id": 1,
  "name": "สายไฟ 2.5 sq.mm",
  "category": "ไฟฟ้า",
  "quantity": 20,
  "unitPrice": 50,
  "threshold": 15
}
```

---

## 9. Business Rules

### Stock

```text
รับสินค้า:
newQuantity = oldQuantity + receiveQuantity

จ่ายสินค้า:
newQuantity = oldQuantity - issueQuantity
```

เงื่อนไข:

```text
issueQuantity > 0
issueQuantity <= currentQuantity
newQuantity >= 0
```

### Low Stock

```text
ถ้า quantity <= threshold
    → สร้าง Notification Event
ถ้า quantity > threshold
    → ไม่สร้าง Notification Event
```

### Stock Valuation

```text
productValue = quantity × unitPrice

categoryValue = ผลรวม productValue ของสินค้าทุกตัวใน category เดียวกัน

totalValue = ผลรวม categoryValue ทุกหมวดหมู่
```

---

## 10. Test Case ที่ควรมี

```text
StockService
│
├── receiveStock()
│   ├── รับสินค้าแล้ว stock เพิ่ม
│   ├── รับจำนวน 0 → reject
│   └── รับจำนวนติดลบ → reject
│
├── issueStock()
│   ├── จ่ายแล้ว stock ลด
│   ├── จ่ายเท่ากับ stock → stock = 0
│   ├── จ่ายเกิน stock → reject
│   ├── จ่าย 0 → reject
│   └── จ่ายจำนวนติดลบ → reject
│
└── checkLowStock()
    ├── stock > threshold → ไม่แจ้ง
    ├── stock = threshold → แจ้ง
    ├── stock < threshold → แจ้ง
    └── stock ต่ำอยู่แล้วและจ่ายซ้ำ → แจ้งตาม transaction ที่กำหนด

ReportService
│
├── calculateProductValue()
├── calculateCategoryValue()
├── calculateTotalValue()
├── quantity = 0 → value = 0
└── unitPrice ไม่มีค่า → error

NotificationService
│
├── EmailNotifier
├── SmsNotifier
├── Email + SMS → เรียกทั้งสองช่องทาง
└── channel failure → stock update ไม่ rollback
```

---

## 11. Acceptance Criteria สำหรับ Reliability

### Scenario: Notification ล้มเหลวแต่ Stock ต้องอัปเดตสำเร็จ

```gherkin
Scenario: Notification ล้มเหลวหลังจากจ่ายสินค้า
  Given สินค้ามีสต็อก 20 หน่วย และ threshold = 15
  And Notification Channel เกิดข้อผิดพลาด
  When พนักงานบันทึกจ่ายออก 8 หน่วย
  Then ระบบอัปเดตสต็อกเป็น 12 หน่วย
  And ระบบบันทึก transaction การจ่ายสินค้าสำเร็จ
  And ระบบไม่ rollback การเปลี่ยนแปลง stock
  And ระบบบันทึกข้อผิดพลาดของ Notification
```

---

## 12. สรุป

ระบบ Inventory นี้ประกอบด้วย Business Logic หลัก 3 ส่วน:

1. **Stock Management** — รับ/จ่ายสินค้า ตรวจสอบจำนวน และป้องกันสต็อกติดลบ
2. **Low Stock Alert** — ตรวจสอบ `stock <= threshold` และสร้าง Notification Event
3. **Stock Valuation** — คำนวณ `quantity × unitPrice` และรวมมูลค่าตามหมวดหมู่

การออกแบบจะแยก Stock Service, Notification Service และ Report Service ออกจากกัน เพื่อให้สามารถทดสอบและดูแลรักษาแต่ละส่วนได้ง่าย และสามารถเพิ่มช่องทางแจ้งเตือนใหม่ในอนาคตโดยไม่กระทบ Stock Business Logic
