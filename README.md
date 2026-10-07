# 📦 Inventory Management System (Team 11)

[![CI Status](https://github.com/phutthapornwo-cpu/team-11-inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/phutthapornwo-cpu/team-11-inventory/actions)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)

ระบบจัดการคลังสินค้าแบบ Command Line Interface (CLI) พัฒนาด้วยภาษา Python ออกแบบมาเพื่อจัดการการเพิ่มสินค้า การปรับอัปเดตสต็อกสินค้าจับต้องได้/ดิจิทัล พร้อมระบบแจ้งเตือนสต็อกต่ำ และการบันทึกข้อมูลลงไฟล์ JSON แบบ Immediate Persistence

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา **Software Engineering in AI Era** ที่ประยุกต์ใช้กระบวนการพัฒนาแบบ Test-Driven Development (TDD), Code Refactoring และ CI/CD Automated Testing

---

## 🚀 ฟีเจอร์หลัก (Key Features)

- **การจัดการสินค้า (Item Management):** เพิ่มรายการสินค้าใหม่ พร้อมตรวจสอบความถูกต้องของข้อมูลและป้องกันรหัสสินค้าซ้ำ
- **การปรับสต็อก (Stock Operations):** รับสินค้าเข้า (`in`) และจ่ายสินค้าออก (`out`) พร้อม Validation ป้องกันสต็อกติดลบ
- **การแจ้งเตือนสต็อกต่ำ (Low Stock Alert):** ค้นหาและเรียงลำดับรายการสินค้าที่มีจำนวนคงเหลือน้อยกว่าหรือเท่ากับเกณฑ์ที่กำหนด (`threshold`)
- **รองรับประเภทสินค้า (Physical vs Digital):** 
  - สินค้าจับต้องได้: ปฏิเสธการขายเมื่อสินค้าไม่พอ และตัดสต็อกอัตโนมัติเมื่อขายสำเร็จ
  - สินค้าดิจิทัล: สต็อกไม่ลดลงเมื่อขาย และจำกัดการเข้าถึงลิงก์ดาวน์โหลดตามสถานะคำสั่งซื้อ
- **การบันทึกข้อมูลทันที (Immediate Persistence):** บันทึกการเปลี่ยนแปลงลงไฟล์ JSON ทันทีเมื่อทำรายการสำเร็จ

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

- **Language:** Python 3.11
- **Testing Framework:** [pytest](https://docs.pytest.org/) & `pytest-cov` (Code Coverage ≥ 85%)
- **Linter & Formatter:** [Ruff](https://docs.astral.sh/ruff/)
- **CI/CD Pipeline:** GitHub Actions (`ci.yml`)

---

## 💻 การติดตั้งและการใช้งาน (Quick Start)

### 1. Clone Repository
```bash
git clone [https://github.com/phutthapornwo-cpu/team-11-inventory.git](https://github.com/phutthapornwo-cpu/team-11-inventory.git)
cd team-11-inventory
