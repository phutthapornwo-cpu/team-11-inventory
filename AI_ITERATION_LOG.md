# AI Iteration Log

## 1. ตารางเปรียบเทียบ ก่อน/หลัง มี Context (ขั้นที่ 4 vs ขั้นที่ 6)

| ประเด็น | ก่อนมี Context (ขั้นที่ 4) | หลังมี Context (ขั้นที่ 6) |
|---|---|---|
| **การแยกไฟล์/ความรับผิดชอบ** | รวมโค้ดทั้งหมดไว้ในไฟล์เดียว | แยกไฟล์ชัดเจน (`models.py`, `notifiers.py`, `service.py`) |
| **Type Hint + Docstring** | ไม่มี Type Hint และ Docstring | มี Type Hint และ Docstring ภาษาไทยทุก method |
| **การผูก Dependency** | `InventoryService` เรียก Notifier ตรงๆ | รับ Dependency ผ่าน Constructor (DI) |
| **การ Hardcode Config** | มีการ Hardcode ค่า Email/เบอร์โทร | แยก Config ออก ไม่ Hardcode ใน Business Logic |

---

## 2. บันทึกการ Iterate ที่ Spec/Context (อย่างน้อย 2 รอบ)

### Iteration รอบที่ 1
* **ผลลัพธ์ที่ผิดพลาด/ปัญหาที่พบ:** (เช่น AI ตีความเงื่อนไขสต็อกต่ำเป็น `<=` แทนที่จะเป็น `<`)
* **สาเหตุ (Spec หรือ Context):** เกิดจาก `specs/spec.md` ในส่วน Acceptance Criteria เขียนเงื่อนไขไม่ชัดเจน
* **การแก้ไขที่ต้นทาง:** เพิ่ม Scenario ใน `specs/spec.md` สำหรับกรณีสต็อกเท่ากับ threshold พอดี
* **ผลลัพธ์หลังแก้ไข:** AI เขียน logic ตรวจสอบเงื่อนไข `<` ได้ถูกต้องตรงตามต้องการ

### Iteration รอบที่ 2
* **ผลลัพธ์ที่ผิดพลาด/ปัญหาที่พบ:** (เช่น AI ใส่ไลบรารี `smtplib` เพื่อส่ง Email จริง)
* **สาเหตุ (Spec หรือ Context):** เกิดจาก AI ละเมิดข้อห้ามใน `.ai-rules.md`
* **การแก้ไขที่ต้นทาง:** ส่ง Prompt ย้ำข้อบังคับ "ห้ามส่ง Email จริง ให้ใช้ print ตามกฎใน .ai-rules.md"
* **ผลลัพธ์หลังแก้ไข:** AI ปรับโค้ดกลับมาใช้ `print` จำลองการส่งข้อความแทน

---

## 3. ประวัติ Prompt และ Tool ที่ใช้
* **AI Tool:** (ระบุ เช่น GitHub Copilot / Gemini / Groq)
* **จำนวน Prompt ที่ใช้:** (บันทึกตามจริง)