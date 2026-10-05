# Lab 04: UX Design, Code Review & AI Code Debugging Summary Report

**สมาชิกในกลุ่ม / ผู้จัดทำ:**
- [ชื่อ-นามสกุล] (รหัสนักศึกษา)

---

## 📂 โครงสร้างไฟล์ใน Lab 04

```text
lab04-ai-coding-ux/
├── README.md                  # สรุปภาพรวมและ Checklist การส่งงาน
├── findings-lab04.md          # ผลการสัมภาษณ์ผู้ใช้ (Needs, Pain Points, POV)
├── persona.md                 # Persona และ Customer Journey Map
├── accessibility-review.md    # รายงานการตรวจ WCAG AA Accessibility Checklist
├── prompt-comparison.md       # การเปรียบเทียบ Prompt สั้น vs Prompt + Context
├── code-review.md             # รายงานการตรวจ Code Review ของโค้ดจาก AI
├── debug-log.md               # สรุป Root Cause Analysis และขั้นตอน Debugging
├── discount.py                # โค้ดคำนวณส่วนลดที่ได้รับการแก้ไข Bug แล้ว
├── assets/
│   ├── wireframe-ai.md        # ASCII Wireframe ที่ให้ AI เจนเนอเรต
│   └── mockup-link.txt        # ลิงก์ Figma / draw.io
└── tests/
    └── test_discount.py       # Unit Test สำหรับทดสอบโมดูล discount.py

---

### 🚀 **คำสั่ง Git สรุปขั้นตอนการส่งงาน (Terminal Commands)**

รันคำสั่งเหล่านี้ใน Terminal เพื่อสร้าง Branch, Commit งาน และ Push ขึ้น GitHub:

```bash
# 1. ตรวจสอบสถานะไฟล์ทั้งหมด
git status

# 2. เพิ่มไฟล์งานทั้งหมดในโฟลเดอร์ lab04-ai-coding-ux
git add lab04-ai-coding-ux/

# 3. Commit งานอย่างเป็นระบบ
git commit -m "feat(lab04): complete UX design, prompt comparison, code review, and debug discount.py"

# 4. Push ขึ้น GitHub (หรือ Push ไปที่ Branch ของคุณ)
git push origin main