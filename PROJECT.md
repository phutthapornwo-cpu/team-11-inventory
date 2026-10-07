# Team 11 - Inventory Management System

> เอกสารบริบทหลักของโครงการสำหรับสมาชิกทีม นักพัฒนา และ AI Coding Agent

---

## 1. Project Overview

**ชื่อโครงการ:** Inventory Management System
**ทีม:** Team 11
**ประเภทระบบ:** Inventory Management System แบบ Command Line Interface (CLI)
**ภาษา:** Python 3.11+
**Repository:** `phutthapornwo-cpu/team-11-inventory`

ระบบนี้ถูกพัฒนาขึ้นเพื่อจัดการข้อมูลสินค้าและจำนวนสินค้าคงเหลือ โดยรองรับการเพิ่มสินค้า การรับสินค้าเข้า การจ่ายสินค้าออก การขายสินค้า การตรวจสอบสต็อกต่ำ และการบันทึกข้อมูลแบบทันทีลงไฟล์ JSON

โครงการเน้นกระบวนการพัฒนาซอฟต์แวร์ที่มีคุณภาพ ได้แก่

* Test-Driven Development (TDD)
* Automated Testing
* Code Refactoring
* Code Review
* CI/CD
* AI-Assisted Development
* Spec-Driven Development

---

# 2. Project Objectives

1. พัฒนาระบบจัดการสินค้าและสต็อกที่ใช้งานผ่าน CLI
2. ป้องกันข้อมูลสต็อกผิดพลาด เช่น จำนวนสินค้าติดลบ
3. รองรับสินค้าหลายประเภท เช่น Physical และ Digital
4. แจ้งเตือนเมื่อสินค้าเหลือในระดับต่ำกว่าเกณฑ์ที่กำหนด
5. บันทึกข้อมูลลง Persistent Storage ทันทีหลังทำรายการสำเร็จ
6. มี Automated Tests เพื่อตรวจสอบความถูกต้องของระบบ
7. ใช้ Code Quality Tools เพื่อตรวจสอบมาตรฐานของ Source Code
8. ใช้ CI/CD เพื่อตรวจสอบโค้ดโดยอัตโนมัติ
9. ออกแบบโครงสร้างให้สามารถเพิ่มความสามารถใหม่ได้ในอนาคต
10. ใช้ AI เป็นเครื่องมือช่วยพัฒนา โดยมนุษย์ยังคงเป็นผู้ตรวจสอบและตัดสินใจขั้นสุดท้าย

---

# 3. Team Members

ทีมพัฒนา **Team 11** ประกอบด้วยสมาชิก 3 คน

| ลำดับ | ชื่อสมาชิก               | บทบาท                             |
| ----: | ------------------------ | --------------------------------- |
|     1 | **Pasin Karunkiat**      | Developer / Refactoring / CI      |
|     2 | **Phutthaporn Wongthai** | Developer / Repository Maintainer |
|     3 | **Thanarat Khumphon**    | Developer / Code Reviewer         |

### Team Responsibilities

สมาชิกทุกคนมีส่วนร่วมในการพัฒนาระบบ โดยรับผิดชอบร่วมกันในด้านต่าง ๆ ได้แก่

* วิเคราะห์ Requirements
* ออกแบบระบบ
* พัฒนา Source Code
* เขียน Automated Tests
* Code Review
* Debugging
* Refactoring
* Documentation
* CI/CD
* AI-Assisted Development

การกำหนดบทบาทข้างต้นเป็นการแบ่งหน้าที่หลักเพื่อช่วยให้การทำงานของทีมชัดเจน แต่สมาชิกทุกคนสามารถช่วยเหลือและ Review งานของสมาชิกคนอื่นได้

---

# 4. Core Features

## 4.1 Product Management

ระบบสามารถจัดการข้อมูลสินค้า ได้แก่

* เพิ่มสินค้าใหม่
* ตรวจสอบข้อมูลสินค้า
* ป้องกันรหัสสินค้าซ้ำ
* ระบุชื่อสินค้า
* ระบุประเภทสินค้า
* ระบุจำนวนสินค้า
* กำหนด Threshold สำหรับการแจ้งเตือนสต็อกต่ำ

---

## 4.2 Stock In

ใช้สำหรับรับสินค้าเข้าคลัง

```text
Product A
Current Stock: 10
Stock In: +5

Result:
Current Stock = 15
```

เมื่อทำรายการสำเร็จ ระบบต้องบันทึกข้อมูลลง Persistent Storage ทันที

---

## 4.3 Stock Out

ใช้สำหรับจ่ายสินค้าออกจากคลัง

ระบบต้องตรวจสอบก่อนดำเนินการว่า

```text
จำนวนที่ต้องการจ่าย <= จำนวนสินค้าคงเหลือ
```

หากสินค้าไม่เพียงพอ ต้องปฏิเสธรายการและไม่ทำให้สต็อกติดลบ

---

## 4.4 Low Stock Alert

ระบบต้องสามารถตรวจสอบสินค้าที่มีจำนวนคงเหลืออยู่ในระดับต่ำ

เงื่อนไข:

```text
stock_quantity <= threshold
```

ตัวอย่าง:

| Product  | Stock | Threshold | Status |
| -------- | ----: | --------: | ------ |
| Keyboard |     2 |         5 | LOW    |
| Mouse    |    10 |         5 | NORMAL |
| Monitor  |     5 |         5 | LOW    |

ฟังก์ชันหลัก:

```python
low_stock_items()
```

---

# 5. Product Types

## 5.1 Physical Product

สินค้าจับต้องได้ เช่น

* Keyboard
* Mouse
* Monitor
* Printer

คุณสมบัติ:

* มีจำนวนสต็อก
* การขายทำให้จำนวนสต็อกลดลง
* ไม่สามารถขายเกินจำนวนที่มีอยู่
* ต้องตรวจสอบ Stock ก่อนทำรายการ

---

## 5.2 Digital Product

สินค้าดิจิทัล เช่น

* Software License
* E-book
* Digital File
* Downloadable Content

คุณสมบัติ:

* ไม่จำเป็นต้องลดจำนวน Stock เมื่อขาย
* สามารถจำกัดการเข้าถึงไฟล์ตามสถานะคำสั่งซื้อ
* ต้องตรวจสอบสถานะการสั่งซื้อก่อนอนุญาตให้ดาวน์โหลด

---

# 6. Data Persistence

ระบบใช้ไฟล์ JSON เป็น Persistent Storage

```text
User Action
     ↓
Validate
     ↓
Business Logic
     ↓
Update Data
     ↓
Save JSON Immediately
```

เมื่อรายการสำเร็จ ระบบต้องบันทึกข้อมูลลงไฟล์ทันที เพื่อป้องกันข้อมูลสูญหายเมื่อโปรแกรมหยุดทำงาน

---

# 7. System Architecture

ระบบแบ่งความรับผิดชอบออกเป็นส่วนต่าง ๆ

```text
CLI / Application
       │
       ▼
Inventory Service
       │
       ├── Product Management
       ├── Stock Operations
       ├── Sales Logic
       └── Low Stock Detection
       │
       ▼
Data / Persistence Layer
       │
       ▼
JSON Storage
```

หลักสำคัญ:

* Business Logic ต้องไม่ผูกติดกับ UI
* ไม่ควร Hardcode Configuration
* ฟังก์ชันควรมีความรับผิดชอบชัดเจน
* สามารถทดสอบ Business Logic ได้โดยไม่ต้องพึ่ง CLI
* ลด Dependency ระหว่าง Module

---

# 8. Project Structure

```text
team-11-inventory/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── diagrams/
│
├── lab04-ai-coding-ux/
│
├── screenshots/
│
├── specs/
│
├── src/
│
├── tests/
│
├── .ai-rules.md
├── AI_ITERATION_LOG.md
├── PROJECT.md
├── README.md
├── RETRO-SPRINT-1.md
├── TEAM_CHARTER.md
├── design_review.md
├── inventory.py
├── update_stock.py
├── pyproject.toml
└── requirements.txt
```

---

# 9. Testing Strategy

โครงการใช้แนวทาง **Test-Driven Development (TDD)** และ Automated Testing

```text
Write Test
    ↓
Test Fails
    ↓
Implement Code
    ↓
Test Passes
    ↓
Refactor
    ↓
Run Tests Again
```

## Test Categories

### Unit Test

ทดสอบฟังก์ชันหรือ Business Logic แยกเป็นส่วน ๆ

ตัวอย่าง:

```text
add_item()
update_stock()
low_stock_items()
```

### Integration Test

ตรวจสอบการทำงานร่วมกันของหลายส่วน

```text
Update Stock
     ↓
Validate
     ↓
Save JSON
```

---

# 10. Code Quality

โครงการใช้ **Ruff** สำหรับตรวจสอบคุณภาพและรูปแบบของ Python Code

```bash
ruff check .
```

ตรวจสอบ Formatting:

```bash
ruff format --check .
```

มาตรฐานการตั้งชื่อ:

```text
Class        → PascalCase
Function     → snake_case
Variable     → snake_case
Constant     → UPPER_CASE
```

---

# 11. Python Coding Standards

ระบบใช้ Python 3.11+

Public Function Signature ควรมี Type Hint

```python
def update_stock(
    product_id: str,
    quantity: int
) -> bool:
    ...
```

Public Method ควรมี Docstring ภาษาไทย

```python
def low_stock_items(self) -> list[Product]:
    """ค้นหารายการสินค้าที่มีจำนวนคงเหลือน้อยกว่าหรือเท่ากับ Threshold."""
```

---

# 12. Design Principles

โครงการยึดหลัก Software Engineering ได้แก่

### Single Responsibility Principle

แต่ละ Module หรือ Function ควรมีหน้าที่หลักที่ชัดเจน

### Open/Closed Principle

ระบบควรสามารถเพิ่มความสามารถใหม่ได้โดยไม่ต้องแก้ Business Logic หลักจำนวนมาก

### Dependency Inversion Principle

Business Logic ไม่ควรผูกติดกับ Implementation เฉพาะตัว

ตัวอย่าง:

```text
Notifier
   │
   ├── EmailNotifier
   ├── SMSNotifier
   └── FutureNotifier
```

---

# 13. Error Handling

ระบบต้องตรวจสอบ Input ก่อนทำ Business Logic

กรณีที่ต้องจัดการ เช่น

* Product ID ไม่มีอยู่ในระบบ
* Product ID ซ้ำ
* จำนวนสินค้าเป็นค่าติดลบ
* จำนวน Stock Out มากกว่า Stock ที่มี
* Threshold ไม่ถูกต้อง
* Product Type ไม่ถูกต้อง
* JSON Data ไม่ถูกต้อง
* ไม่สามารถบันทึกข้อมูลได้

ตัวอย่าง Error:

```text
Invalid quantity
Insufficient stock
Product not found
Duplicate product ID
Invalid threshold
```

Error ที่เกิดขึ้นต้องไม่ทำให้ข้อมูล Stock อยู่ในสถานะไม่ถูกต้อง

---

# 14. Data Integrity

หลักสำคัญของระบบ:

> ห้ามทำให้จำนวน Stock ติดลบ

ทุกการเปลี่ยนแปลง Stock ต้องผ่าน Validation ก่อน

```text
Request
   ↓
Validate Input
   ↓
Check Product
   ↓
Check Stock
   ↓
Update
   ↓
Persist
```

หาก Validation ไม่ผ่าน:

```text
Do NOT modify stock
Do NOT persist invalid state
```

---

# 15. Immediate Persistence

หลังจาก Business Operation สำเร็จ ระบบต้องบันทึกข้อมูลทันที

```text
Stock = 10

User performs Stock In +5

Stock = 15
      ↓
Save JSON immediately
```

ไม่ควรรอให้โปรแกรมปิดก่อนจึงค่อยบันทึกข้อมูล

---

# 16. CI/CD

โครงการใช้ GitHub Actions สำหรับ Automated Quality Checks

Pipeline:

```text
Install Dependencies
        ↓
Run Tests
        ↓
Run Coverage
        ↓
Run Ruff
        ↓
Pass / Fail
```

CI ต้องไม่ผ่านหาก:

* Test Fail
* Coverage ต่ำกว่าเกณฑ์
* Ruff พบข้อผิดพลาดที่กำหนดให้เป็น Failure

---

# 17. Local Development

## Clone Repository

```bash
git clone https://github.com/phutthapornwo-cpu/team-11-inventory.git
cd team-11-inventory
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python inventory.py
```

## Run Tests

```bash
pytest tests/ -v
```

## Run Coverage

```bash
pytest --cov=. --cov-report=term-missing
```

## Run Ruff

```bash
ruff check .
```

---

# 18. Git Workflow

สมาชิกทีมควรทำงานผ่าน Feature Branch

```text
main
 │
 ├── feat/low-stock-alert
 ├── feat/stock-operation
 ├── fix/stock-validation
 └── refactor/inventory-service
```

Workflow:

```text
Create Branch
     ↓
Implement
     ↓
Run Tests
     ↓
Run Ruff
     ↓
Commit
     ↓
Push
     ↓
Pull Request
     ↓
Code Review
     ↓
Merge
```

ไม่ควร Push การเปลี่ยนแปลงที่ยังไม่ผ่าน Test โดยตรงเข้า `main`

---

# 19. Commit Convention

แนะนำให้ใช้ Conventional Commits

```text
feat: add low stock alert
fix: prevent negative stock
test: add low stock test cases
refactor: separate stock service
docs: update project documentation
ci: improve github actions workflow
```

---

# 20. AI-Assisted Development

AI สามารถใช้เพื่อช่วย:

* วิเคราะห์ Requirement
* เสนอ Implementation
* เขียน Unit Test
* Refactor Code
* วิเคราะห์ Bug
* Review Code
* สร้าง Documentation

แต่ AI ไม่ควรเป็นผู้ตัดสินใจขั้นสุดท้ายโดยไม่มี Human Review

กระบวนการ:

```text
Requirement
     ↓
Human Understanding
     ↓
AI Assistance
     ↓
Developer Review
     ↓
Run Tests
     ↓
Code Review
     ↓
Merge
```

AI-generated Code ทุกส่วนต้องผ่านการตรวจสอบก่อนนำเข้าสู่ `main`

---

# 21. Specification-Driven Development

ก่อนพัฒนาฟีเจอร์ใหม่ควรเริ่มจาก Specification

```text
Requirement
    ↓
User Story
    ↓
Acceptance Criteria
    ↓
Test Cases
    ↓
Implementation
    ↓
Refactoring
    ↓
Final Verification
```

Acceptance Criteria ต้องสามารถแปลงเป็น Test Case ได้

ตัวอย่าง:

```text
Given:
สินค้าเหลือ 5 ชิ้น
Threshold = 5

When:
ระบบตรวจสอบ Low Stock

Then:
สินค้าต้องถูกจัดเป็น Low Stock
```

---

# 22. Definition of Done

Feature จะถือว่าเสร็จเมื่อผ่านเงื่อนไขทั้งหมด

* [ ] Requirement ชัดเจน
* [ ] มี Acceptance Criteria
* [ ] มี Test Case
* [ ] Implementation เสร็จ
* [ ] Unit Tests ผ่าน
* [ ] Integration Tests ผ่าน หากเกี่ยวข้อง
* [ ] Coverage ผ่านเกณฑ์
* [ ] Ruff ผ่าน
* [ ] ไม่มี Business Logic ที่ซ้ำซ้อน
* [ ] ไม่มี Hardcoded Configuration ที่ไม่เหมาะสม
* [ ] Documentation ถูกอัปเดต
* [ ] Code Review ผ่าน
* [ ] CI ผ่าน
* [ ] สามารถ Merge ได้โดยไม่ทำให้ Feature เดิมเสีย

---

# 23. Important Constraints

## ห้าม

* Hardcode Business Configuration
* ใช้ Global Variable โดยไม่จำเป็น
* ทำให้ Stock ติดลบ
* ข้าม Validation
* รวม Business Logic และ I/O ไว้ใน Function เดียวโดยไม่จำเป็น
* แก้ Test เพื่อให้ Test ผ่านโดยไม่แก้ Root Cause
* ลบ Test ที่กำลัง Fail เพื่อหลีกเลี่ยงปัญหา
* Commit Secret หรือ Credential

## ต้อง

* ใช้ Type Hint
* เขียน Test สำหรับ Feature ใหม่
* ตรวจสอบ Edge Cases
* Run Test ก่อน Commit
* Run Ruff ก่อน Pull Request
* Update Documentation เมื่อ Behavior ของระบบเปลี่ยน
* Review AI-generated Code ก่อน Merge

---

# 24. Project Documentation

| File / Directory      | Purpose                         |
| --------------------- | ------------------------------- |
| `PROJECT.md`          | Project Context และกฎภาพรวม     |
| `README.md`           | ภาพรวมและ Quick Start           |
| `.ai-rules.md`        | Rules สำหรับ AI Agent           |
| `specs/`              | Requirements และ Specifications |
| `tests/`              | Automated Tests                 |
| `diagrams/`           | System / Architecture Diagrams  |
| `AI_ITERATION_LOG.md` | บันทึกการใช้ AI                 |
| `TEAM_CHARTER.md`     | กติกาและการทำงานของทีม          |
| `RETRO-SPRINT-1.md`   | Sprint Retrospective            |
| `design_review.md`    | Design Review                   |

---

# 25. Project Success Criteria

โครงการถือว่าประสบความสำเร็จเมื่อระบบสามารถ:

1. เพิ่มสินค้าได้อย่างถูกต้อง
2. ป้องกัน Product ID ซ้ำ
3. รับสินค้าเข้าได้
4. จ่ายสินค้าออกได้
5. ป้องกัน Stock ติดลบ
6. รองรับ Physical และ Digital Product
7. ตรวจสอบ Low Stock ได้
8. บันทึกข้อมูลลง Persistent Storage ทันที
9. Automated Tests ผ่าน
10. Code Coverage ผ่านเกณฑ์
11. Ruff ผ่าน
12. CI/CD ทำงานได้
13. Code สามารถ Maintain และ Extend ได้
14. Documentation สอดคล้องกับ Implementation
15. AI-assisted Code ผ่าน Human Review

---

# 26. Final Development Principle

> **Build the right behavior, prove it with tests, keep the design maintainable, and let humans remain responsible for the final decision.**

Team 11 ให้ความสำคัญกับการพัฒนาซอฟต์แวร์อย่างเป็นระบบ ไม่ใช่เพียงการเขียนโค้ดให้สามารถทำงานได้ แต่ต้องสามารถอธิบาย ทดสอบ ตรวจสอบ และบำรุงรักษาระบบได้ในระยะยาว
