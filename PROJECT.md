# Team 11 - Inventory Management System
> ระบบจัดการคลังสินค้าแบบ CLI พัฒนาด้วยภาษา Python พร้อมชุดทดสอบอัตโนมัติ (TDD) และการตรวจสอบคุณภาพโค้ดด้วย CI/CD

---

## 1. ข้อมูลทั่วไป (Project Overview)
- **ชื่อทีม:** Team 11
- **สมาชิกในทีม:**
  1. นายพศิน การุณเกียรติ (Pasin Karunkiat) - Core Developer / Refactoring & CI Setup
  2. พุทธพร วงษ์ไทย (Phutthaporn Wongthai) - Core Developer / Repo Owner
  3. ธนรัฐ ขุมพร (Thanarat Khumphon) - Core Developer / Reviewer
- **Repository:** [phutthapornwo-cpu/team-11-inventory](https://github.com/phutthapornwo-cpu/team-11-inventory)
- **สไลด์นำเสนอ (Slide):** [สไลด์นำเสนอโครงงาน](https://docs.google.com/presentation) *(อัปเดตลิงก์จริงของทีม)*

---

## 2. ดรรชนีเอกสารและ Artifacts (Artifact Index)

| รายการ Artifact | สรุปเนื้อหาโดยสังเขป | ตำแหน่งไฟล์/ลิงก์ (File Path) |
| :--- | :--- | :--- |
| **Requirements & Spec** | User Stories, Acceptance Criteria (AC) การจัดการสต็อก และสินค้าจับต้องได้/ดิจิทัล | [`docs/requirements.md`](./docs/requirements.md) |
| **Tech Stack** | Python 3.11, pytest, pytest-cov, ruff, GitHub Actions | [`docs/tech-stack.md`](./docs/tech-stack.md) |
| **Architecture** | โครงสร้างโมดูล CLI, Data Model และการบันทึกข้อมูลลง JSON แบบ Immediate Persistence | [`docs/architecture.md`](./docs/architecture.md) |
| **ADR (Decision Records)** | บันทึกการตัดสินใจทางสถาปัตยกรรม (เช่น การเลือกใช้ JSON, Pytest, Ruff) | [`docs/adr/`](./docs/adr/) |
| **AI Use Log** | บันทึกประวัติและข้อความ Prompt ในการใช้ AI ช่วยพัฒนาตลอดภาคการศึกษา | [`AI_USE_LOG.md`](./AI_USE_LOG.md) |
| **Ethics Review** | การวิเคราะห์ประเด็นจริยธรรม 4 ข้อ (ความรับผิดชอบ, ลิขสิทธิ์, PDPA, อคติ AI) | [`ethics.md`](./ethics.md) |
| **Code Review Log** | สรุปประวัติและตารางการตรวจทานโค้ดจาก Lab 4 | [`lab04-ai-coding-ux/code-review.md`](./lab04-ai-coding-ux/code-review.md) |
| **Test Gap & Coverage** | ตารางวิเคราะห์กรณีทดสอบที่ AI มองข้าม และบันทึกผล Coverage | [`test-gap.md`](./test-gap.md), [`coverage-note.md`](./coverage-note.md) |
| **Code Smells & Refactoring** | จุดที่อ่านยากใน legacy code และบันทึกผล Characterization Test | [`smells.md`](./smells.md) |

---

## 3. โครงสร้างการทดสอบและการประเมิน (Testing & Evals)
- **Unit & Integration Tests:** อยู่ในโฟลเดอร์ [`tests/`](./tests/) 
  - `tests/test_inventory.py` (ระบบคลังสินค้าและการเตือนสต็อกต่ำ `low_stock_items`)
  - `tests/test_pricing_legacy.py` (Characterization Tests สำหรับโมดูลคิดราคา)
- **CI Workflow & Quality Checks:** ควบคุมด้วย GitHub Actions [`ci.yml`](./.github/workflows/ci.yml)
  - กำหนดเกณฑ์ Code Coverage ขั้นต่ำไว้ที่ **85%** (`--cov-fail-under=85`)
  - ตรวจสอบ Linting และ Code Format ด้วย **Ruff**

---

## 4. วิธีการรันโครงการแบบ Local (Quick Start)

```bash
# 1. Clone repository
git clone [https://github.com/phutthapornwo-cpu/team-11-inventory.git](https://github.com/phutthapornwo-cpu/team-11-inventory.git)
cd team-11-inventory

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Tests and Linting
pytest tests/ -v
ruff check .

# 4. Run Main Application (CLI)
python inventory.py
