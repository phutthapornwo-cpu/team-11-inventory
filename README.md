# 📦 Inventory Management System — Team 11

[![CI Status](https://github.com/phutthapornwo-cpu/team-11-inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/phutthapornwo-cpu/team-11-inventory/actions)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-Ruff-000000.svg)
![Test Coverage](https://img.shields.io/badge/coverage-%E2%89%A585%25-brightgreen.svg)

ระบบจัดการคลังสินค้าแบบ **Command Line Interface (CLI)** พัฒนาด้วยภาษา **Python 3.11** สำหรับจัดการข้อมูลสินค้า การรับสินค้าเข้า การจ่ายสินค้าออก การขายสินค้า การตรวจสอบสต็อก และการแจ้งเตือนเมื่อสินค้ามีจำนวนต่ำกว่าเกณฑ์ที่กำหนด

ระบบรองรับทั้ง **สินค้าจับต้องได้ (Physical Product)** และ **สินค้าดิจิทัล (Digital Product)** พร้อมการตรวจสอบข้อมูลและการบันทึกข้อมูลลงไฟล์ JSON แบบ **Immediate Persistence**

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา **Software Engineering in AI Era** โดยประยุกต์ใช้แนวทาง **Test-Driven Development (TDD), Automated Testing, Code Refactoring, Code Review และ CI/CD**

---

## 👥 Team Members

|  # | Member                   | Responsibility                    |
| -: | ------------------------ | --------------------------------- |
|  1 | **Pasin Karunkiat**      | Developer / Refactoring / CI      |
|  2 | **Phutthaporn Wongthai** | Developer / Repository Maintainer |
|  3 | **Thanarat Khumphon**    | Developer / Code Reviewer         |

สมาชิกทุกคนมีส่วนร่วมในการวิเคราะห์ Requirements, ออกแบบระบบ, พัฒนา Source Code, เขียน Test, Debug, Code Review และจัดทำ Documentation

---

## 🚀 Key Features

### 📦 1. Item Management

จัดการข้อมูลสินค้า โดยระบบสามารถ:

* เพิ่มสินค้าใหม่
* ตรวจสอบความถูกต้องของข้อมูล
* ป้องกันรหัสสินค้าซ้ำ
* กำหนดประเภทสินค้า
* กำหนดจำนวน Stock
* กำหนด Stock Threshold

---

### 📥 2. Stock In / Stock Out

รองรับการปรับจำนวนสินค้าในคลัง:

```text
Stock In
   ↓
เพิ่มจำนวนสินค้า
```

```text
Stock Out
   ↓
ตรวจสอบ Stock
   ↓
เพียงพอ?
 ┌─┴─┐
Yes  No
 ↓    ↓
ลด   Reject
Stock
```

ระบบจะไม่อนุญาตให้ Stock ติดลบ และจะปฏิเสธรายการหากจำนวนสินค้าที่ต้องการจ่ายมากกว่าจำนวนที่มีอยู่

---

### 🔔 3. Low Stock Alert

ระบบสามารถค้นหาสินค้าที่มีจำนวนคงเหลือน้อยกว่าหรือเท่ากับ Threshold

เงื่อนไข:

```text
stock_quantity <= threshold
```

ตัวอย่าง:

| Product  | Stock | Threshold | Status    |
| -------- | ----: | --------: | --------- |
| Keyboard |     2 |         5 | 🔴 LOW    |
| Mouse    |    10 |         5 | 🟢 NORMAL |
| Monitor  |     5 |         5 | 🔴 LOW    |

รายการสินค้าที่อยู่ในระดับต่ำสามารถนำไปใช้สำหรับการแจ้งเตือนหรือการวางแผนเติมสินค้า

---

### 🖥️ 4. Physical Product

สำหรับสินค้าที่จับต้องได้ เช่น:

* Keyboard
* Mouse
* Monitor
* Printer

เมื่อมีการขายสินค้า ระบบจะตรวจสอบจำนวน Stock ก่อน และตัด Stock เมื่อการขายสำเร็จ

```text
Current Stock
      ↓
Check Availability
      ↓
Stock Sufficient?
      ↓
   Sell Product
      ↓
Decrease Stock
      ↓
Save Data
```

---

### 💾 5. Digital Product

รองรับสินค้าดิจิทัล เช่น:

* Software License
* E-book
* Digital File

สำหรับ Digital Product:

* ไม่ลดจำนวน Stock เมื่อขาย
* ตรวจสอบสถานะคำสั่งซื้อ
* จำกัดการเข้าถึง Download Link ตามเงื่อนไขของระบบ

---

### 💽 6. Immediate Persistence

ทุกการเปลี่ยนแปลงข้อมูลที่สำเร็จจะถูกบันทึกลงไฟล์ JSON ทันที

```text
User Action
     ↓
Validation
     ↓
Business Logic
     ↓
Update Data
     ↓
Save JSON
```

ช่วยลดความเสี่ยงที่ข้อมูลจะสูญหายเมื่อโปรแกรมหยุดทำงานหรือถูกปิดกะทันหัน

---

# 🛠️ Tech Stack

| Technology         | Purpose                    |
| ------------------ | -------------------------- |
| **Python 3.11**    | Programming Language       |
| **pytest**         | Automated Testing          |
| **pytest-cov**     | Code Coverage              |
| **Ruff**           | Linting & Formatting       |
| **JSON**           | Data Persistence           |
| **Git**            | Version Control            |
| **GitHub**         | Repository & Collaboration |
| **GitHub Actions** | CI/CD                      |

### Quality Target

```text
Code Coverage ≥ 85%
```

---

# 🏗️ System Architecture

ภาพรวมการทำงานของระบบ:

```text
┌─────────────────────┐
│       CLI User      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Inventory Management│
│       Logic         │
└──────────┬──────────┘
           │
     ┌─────┼─────┐
     │     │     │
     ▼     ▼     ▼
  Product Stock  Low
  Manager  Ops  Stock
     │     │     │
     └─────┼─────┘
           │
           ▼
┌─────────────────────┐
│   JSON Persistence  │
└─────────────────────┘
```

---

# 📁 Project Structure

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

# 💻 Quick Start

## 1. Requirements

ก่อนเริ่มใช้งาน ตรวจสอบว่ามี:

* Python 3.11+
* pip
* Git

ตรวจสอบ Python:

```bash
python --version
```

ตัวอย่าง:

```text
Python 3.11.x
```

---

## 2. Clone Repository

```bash
git clone https://github.com/phutthapornwo-cpu/team-11-inventory.git
cd team-11-inventory
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Application

```bash
python inventory.py
```

---

# 🧪 Testing

## Run All Tests

```bash
pytest tests/ -v
```

ตัวอย่างผลลัพธ์:

```text
============================= test session starts =============================

tests/test_inventory.py ............                         [100%]

============================== 100% passed ===============================
```

---

## 📊 Test Coverage

ตรวจสอบ Code Coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

เป้าหมาย:

```text
Coverage ≥ 85%
```

Coverage ช่วยให้ทีมตรวจสอบว่ามีส่วนใดของ Source Code ที่ยังไม่มี Test ครอบคลุม

---

# 🔍 Code Quality

ตรวจสอบ Code ด้วย Ruff:

```bash
ruff check .
```

ตรวจสอบ Formatting:

```bash
ruff format --check .
```

ก่อนสร้าง Pull Request ควรตรวจสอบ:

```bash
pytest tests/ -v
ruff check .
ruff format --check .
```

---

# 🔄 CI/CD

โปรเจกต์ใช้ **GitHub Actions** สำหรับตรวจสอบคุณภาพของ Source Code โดยอัตโนมัติ

Pipeline โดยสรุป:

```text
Push / Pull Request
        ↓
Install Dependencies
        ↓
Run Tests
        ↓
Check Coverage
        ↓
Run Ruff
        ↓
   ┌────┴────┐
   ▼         ▼
 PASS       FAIL
   │         │
   ▼         ▼
Merge     Fix Code
```

สามารถดูสถานะ CI ได้จาก:

**GitHub Actions**

---

# 🌿 Git Workflow

ทีมใช้ Feature Branch เพื่อแยกการพัฒนาแต่ละ Feature

ตัวอย่าง:

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
Develop
     ↓
Write / Update Tests
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

---

# 📝 Commit Convention

ทีมแนะนำให้ใช้ Conventional Commits

### Feature

```bash
git commit -m "feat: add low stock alert"
```

### Bug Fix

```bash
git commit -m "fix: prevent negative stock"
```

### Test

```bash
git commit -m "test: add low stock test cases"
```

### Refactoring

```bash
git commit -m "refactor: improve inventory service"
```

### Documentation

```bash
git commit -m "docs: update project documentation"
```

### CI/CD

```bash
git commit -m "ci: improve github actions workflow"
```

---

# 🤖 AI-Assisted Development

โครงการนี้ประยุกต์ใช้ AI เพื่อช่วยในกระบวนการพัฒนาซอฟต์แวร์ เช่น:

* วิเคราะห์ Requirements
* ออกแบบแนวทางแก้ปัญหา
* สร้าง Test Cases
* เขียน Source Code
* Debugging
* Refactoring
* Code Review
* Documentation

อย่างไรก็ตาม **AI ไม่ได้เป็นผู้ตัดสินใจขั้นสุดท้าย**

โค้ดที่สร้างโดย AI ต้องผ่านการตรวจสอบและทดสอบโดยสมาชิกทีมก่อนนำไปใช้งานจริง

```text
Requirement
     ↓
Human Analysis
     ↓
AI Assistance
     ↓
Developer Review
     ↓
Automated Tests
     ↓
Code Review
     ↓
Merge
```

---

# 📋 Specification-Driven Development

การพัฒนา Feature ใหม่ควรเริ่มจาก Specification

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
Verification
```

Specification ของระบบอยู่ภายใน:

```text
specs/
```

---

# ✅ Definition of Done

Feature จะถือว่าเสร็จเมื่อผ่านเงื่อนไขสำคัญดังต่อไปนี้:

* [ ] Requirement ชัดเจน
* [ ] Acceptance Criteria ครบถ้วน
* [ ] มี Test Case
* [ ] Implementation เสร็จสมบูรณ์
* [ ] Tests ผ่าน
* [ ] Coverage ผ่านเกณฑ์
* [ ] Ruff ผ่าน
* [ ] Code Review ผ่าน
* [ ] CI ผ่าน
* [ ] Documentation อัปเดต

---

# 📚 Documentation

เอกสารสำคัญภายใน Repository:

| File / Directory      | Description                                |
| --------------------- | ------------------------------------------ |
| `README.md`           | ภาพรวมและวิธีใช้งานโปรเจกต์                |
| `PROJECT.md`          | Project Context และ Development Guidelines |
| `.ai-rules.md`        | Rules สำหรับ AI Coding Agent               |
| `specs/`              | Requirements และ Specifications            |
| `tests/`              | Automated Tests                            |
| `diagrams/`           | System และ Architecture Diagrams           |
| `TEAM_CHARTER.md`     | กติกาการทำงานของทีม                        |
| `AI_ITERATION_LOG.md` | บันทึกการใช้ AI                            |
| `RETRO-SPRINT-1.md`   | Sprint Retrospective                       |
| `design_review.md`    | Design Review                              |

---

# 🎯 Project Goals

ระบบมีเป้าหมายหลักในการ:

1. จัดการข้อมูลสินค้าได้อย่างถูกต้อง
2. ป้องกัน Stock ติดลบ
3. ตรวจสอบสินค้าที่มี Stock ต่ำ
4. บันทึกข้อมูลอย่างต่อเนื่องและปลอดภัย
5. มี Automated Tests ที่ครอบคลุม
6. รักษา Code Quality
7. ใช้ CI/CD ในการตรวจสอบอัตโนมัติ
8. พัฒนาระบบให้สามารถ Maintain และ Extend ได้
9. ประยุกต์ใช้ AI อย่างเหมาะสมในกระบวนการพัฒนา
10. ให้ Human Review เป็นส่วนสำคัญก่อน Merge Code

---

# 📌 Important Rule

> **Stock ต้องไม่ติดลบ**

ทุกการเปลี่ยนแปลง Stock ต้องผ่าน Validation ก่อนดำเนินการ

```text
Request
   ↓
Validate
   ↓
Check Stock
   ↓
Update
   ↓
Persist
```

หาก Validation ไม่ผ่าน ระบบต้อง:

```text
❌ ไม่แก้ไข Stock
❌ ไม่บันทึกข้อมูลที่ไม่ถูกต้อง
```

---

# 🔗 Repository

**GitHub Repository**

https://github.com/phutthapornwo-cpu/team-11-inventory

---

# 👥 Team 11

### Inventory Management System

Developed by:

* **Pasin Karunkiat**
* **Phutthaporn Wongthai**
* **Thanarat Khumphon**

---

## 📄 License

This project is developed for **educational and academic purposes** as part of the Software Engineering in AI Era course.
