| ประเด็น | ก่อนมี context (ขั้นที่ 4) | หลังมี context (ขั้นที่ 6) |
|---|---|---|
| แยกไฟล์/ความรับผิดชอบ | โค้ดรวมหลายหน้าที่ในไฟล์เดียว | แยกเป็น `src/models.py`, `src/notifiers.py`, `src/service.py` ตาม SRP |
| type hint + docstring | ใช้ไม่ครบ/ไม่สม่ำเสมอ | ใส่ type hint ทุก signature และ docstring ไทยใน public method |
| service ผูกกับ notifier ตรง ๆ หรือไม่ | มีโอกาสผูกกับ implementation ตรง | `InventoryService` รับ `Notifier` ผ่าน constructor (DIP) ไม่รู้จัก Email/SMS โดยตรง |
| hardcode config หรือไม่ | เสี่ยง hardcode ช่องทางหรือปลายทางแจ้งเตือน | ใช้ `NotifierFactory` รับ config จากภายนอก ไม่มี hardcode ใน business logic |
