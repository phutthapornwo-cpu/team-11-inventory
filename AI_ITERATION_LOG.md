## AI Iteration Log: Before and After Context

### Objective

เปรียบเทียบผลลัพธ์จากการใช้ AI ช่วยพัฒนาระบบ Inventory Management System ระหว่างขั้นที่ 4 ซึ่งมีบริบทของโปรเจกต์ไม่เพียงพอ และขั้นที่ 6 ซึ่งให้ Context, Architecture และข้อกำหนดด้านคุณภาพโค้ดอย่างชัดเจน

### Comparison: Step 4 vs Step 6

| ประเด็น | ก่อนมี Context (ขั้นที่ 4) | หลังมี Context (ขั้นที่ 6) |
|---|---|---|
| การแยกไฟล์และความรับผิดชอบ (SRP) | โค้ดมีแนวโน้มรวมหลายหน้าที่ไว้ในไฟล์เดียว ทำให้ดูแลและทดสอบแยกส่วนได้ยาก | แยกเป็น `src/models.py`, `src/notifiers.py` และ `src/service.py` ตามหน้าที่ของแต่ละโมดูล |
| Type Hint และ Docstring | ใช้ Type Hint และ Docstring ไม่ครบถ้วนหรือไม่สม่ำเสมอ | กำหนด Type Hint ให้ทุก Function/Method Signature และเขียน Docstring ภาษาไทยสำหรับ Public Method |
| การผูกกับ Notifier (DIP) | มีความเสี่ยงที่ Business Logic จะผูกกับ Implementation ของระบบแจ้งเตือนโดยตรง | `InventoryService` รับ Dependency ประเภท `Notifier` ผ่าน Constructor ทำให้ไม่ต้องรู้รายละเอียดของ Email หรือ SMS โดยตรง |
| การจัดการ Configuration | มีความเสี่ยงที่จะ Hardcode ช่องทางหรือปลายทางการแจ้งเตือนไว้ใน Business Logic | ใช้ `NotifierFactory` รับ Configuration จากภายนอก เพื่อแยกการสร้าง Notifier ออกจาก Business Logic |
| ความสามารถในการทดสอบ | หาก Business Logic ผูกกับระบบแจ้งเตือนจริง การทดสอบอาจต้องพึ่งพา External Service | สามารถส่ง Mock หรือ Fake Notifier เข้าไปทดสอบได้ โดยไม่จำเป็นต้องเรียกบริการแจ้งเตือนจริง |
| ความสามารถในการขยายระบบ | การเพิ่มช่องทางแจ้งเตือนอาจต้องแก้ไขโค้ดหลายส่วน | สามารถเพิ่ม Implementation ของ Notifier ใหม่ได้ โดยลดการเปลี่ยนแปลงใน `InventoryService` |
| ความสามารถในการบำรุงรักษา | ความรับผิดชอบที่ปะปนกันทำให้แก้ไขและตรวจสอบสาเหตุของปัญหาได้ยากขึ้น | โครงสร้างแยกส่วนชัดเจน ช่วยให้ตรวจสอบ แก้ไข และพัฒนาต่อได้ง่ายขึ้น |

### Key Improvements

1. **Single Responsibility Principle (SRP)**  
   แยก Model, Notification และ Service ออกจากกัน โดยแต่ละโมดูลมีหน้าที่ชัดเจน

2. **Dependency Inversion Principle (DIP)**  
   ให้ `InventoryService` พึ่งพา Abstraction ของ Notifier แทนการผูกกับ Implementation เฉพาะ

3. **Dependency Injection**  
   ส่ง Notifier ผ่าน Constructor เพื่อให้เปลี่ยน Implementation และทดสอบด้วย Test Double ได้สะดวก

4. **Separation of Configuration**  
   แยก Configuration ของช่องทางแจ้งเตือนออกจาก Business Logic เพื่อให้ปรับเปลี่ยนการตั้งค่าได้โดยไม่ต้องแก้โค้ดส่วนหลัก

5. **Improved Maintainability and Testability**  
   โครงสร้างที่ชัดเจนช่วยให้การทดสอบ การตรวจสอบข้อผิดพลาด และการเพิ่มความสามารถใหม่ทำได้ง่ายขึ้น

### Lessons Learned

การใช้ AI ให้ได้ผลลัพธ์ที่มีคุณภาพไม่ได้ขึ้นอยู่กับการเขียน Prompt เพียงอย่างเดียว แต่ขึ้นอยู่กับ Context ที่ให้แก่ AI ด้วย เช่น โครงสร้าง Repository, ข้อกำหนดของระบบ, หลักการออกแบบซอฟต์แวร์ และแนวทางการทดสอบ

เมื่อระบุข้อกำหนดเหล่านี้อย่างชัดเจน AI จะสามารถเสนอแนวทางที่สอดคล้องกับ Architecture ของโปรเจกต์ได้ดีขึ้น อย่างไรก็ตาม ผลลัพธ์ที่ได้ยังต้องผ่านการตรวจสอบจากนักพัฒนาและการทดสอบจริงก่อนนำไปใช้งาน

### Verification Checklist

- [ ] ตรวจสอบว่าแต่ละโมดูลมีความรับผิดชอบตรงตามที่กำหนด
- [ ] ตรวจสอบ Type Hint และ Docstring ใน Public API
- [ ] ตรวจสอบว่า `InventoryService` รับ Notifier ผ่าน Constructor
- [ ] ตรวจสอบว่า Business Logic ไม่ผูกกับ Email/SMS Implementation โดยตรง
- [ ] ตรวจสอบว่า Configuration ไม่ถูก Hardcode ไว้ใน Business Logic
- [ ] ทดสอบด้วย Mock หรือ Fake Notifier
- [ ] รัน Automated Tests และตรวจสอบผลลัพธ์จริง
- [ ] ตรวจสอบ Code Quality ด้วย Ruff และ Code Review

**หมายเหตุ:** รายการตรวจสอบข้างต้นเป็นเกณฑ์สำหรับยืนยันผลการปรับปรุง ไม่ควรทำเครื่องหมายผ่านจนกว่าจะตรวจสอบโค้ดและผลการทดสอบจริงแล้ว
