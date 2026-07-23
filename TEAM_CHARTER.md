# TEAM_CHARTER.md

## สมาชิกและบทบาท

| ชื่อ | GitHub Username | บทบาท |
|---|---|---|
| นาย พุทธพร วงษ์ไทย  | phutthaporn wongthai | Product Owner |
| นาย ธนารัตน์ คุ้มผล | thanarat-kh | Scrum Master / Developer |
| นาย พศิน การุณเกียรติ์ | pasin-karunkiat | Developer |

## Branching Strategy

ทีมใช้ GitHub Flow:
- main branch ต้อง deploy ได้เสมอ ห้าม commit โดยตรง
- ทุก feature ใหม่ต้องสร้าง branch ชื่อ feat/<issue-number>-<short-name>
- ทุก PR ต้องมีคนอื่นในทีมอย่างน้อย 1 คน review และ approve ก่อน merge

## Sprint Goal (Sprint 1)

Sprint นี้ทีมจะส่งมอบ US-02 (เพิ่มสินค้าใหม่) และ US-03 (ปรับปรุงยอดสต็อก) ที่ทำงานผ่าน CLI ได้จริง บันทึกข้อมูลคงทน และผ่าน Acceptance Criteria ครบถ้วน

## AI Usage Policy

- ใช้ AI ช่วยเขียน draft code และ draft commit message ได้
- ทุก commit message ที่ AI generate ต้องอ่านและแก้ให้ตรงกับ diff จริงก่อน commit
- ห้าม copy code จาก AI โดยไม่อ่านและทำความเข้าใจก่อน
- ใช้เฉพาะ AI ที่ไม่มีค่าใช้จ่าย ไม่บังคับซื้อ subscription
