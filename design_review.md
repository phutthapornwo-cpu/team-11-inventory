## ตารางวิเคราะห์

| หลัก SOLID | ละเมิดหรือไม่ | จุดที่เกี่ยวข้อง (class/method) | อธิบาย/ผลกระทบ | ข้อเสนอปรับปรุง |
|---|---|---|---|---|
| **S (SRP)** |  ไม่ละเมิด | `Product`, `InventoryService`, `EmailNotifier`, `SMSNotifier` | แต่ละ class มีหน้าที่ค่อนข้างชัดเจน เช่น `Product` จัดการข้อมูล/กฎของสินค้า, `InventoryService` จัดการ stock, `Notifier` จัดการการแจ้งเตือน | โครงสร้างปัจจุบันเหมาะสม สามารถคงไว้ได้ |
| **O (OCP)** |  ละเมิด | `NotifierFactory.create_notifier()` | มี `if` แยกตาม channel (`email`, `sms`) หากเพิ่มช่องทางใหม่ เช่น LINE หรือ Slack ต้องกลับมาแก้ไข method นี้ ทำให้ไม่ปิดต่อการแก้ไข | ใช้ **Factory Registry / Dictionary** สำหรับลงทะเบียน notifier ใหม่ โดยไม่ต้องเพิ่ม `if` ใน method เดิม |
| **L (LSP)** |  ไม่ละเมิด | `Notifier`, `EmailNotifier`, `SMSNotifier` | `EmailNotifier` และ `SMSNotifier` สามารถใช้แทน `Notifier` ได้ เพราะมี `send_low_stock_alert(Product)` ตาม contract เดียวกัน | คง interface/contract ของ `Notifier` ให้เหมือนเดิม |
| **I (ISP)** |  ไม่ละเมิด | `Notifier` | `Notifier` มีเพียง method `send_low_stock_alert()` จึงเป็น interface ขนาดเล็ก และ implementation ไม่ต้อง implement method ที่ไม่จำเป็น | โครงสร้างปัจจุบันเหมาะสม ไม่จำเป็นต้องแยก interface เพิ่ม |
| **D (DIP)** |  ไม่ละเมิด | `InventoryService.__init__()` | `InventoryService` รับ `Iterable[Notifier]` ซึ่งเป็น abstraction แทนการผูกโดยตรงกับ `EmailNotifier` หรือ `SMSNotifier` ทำให้เปลี่ยน/ทดสอบ notifier ได้ง่าย | คงการ inject `Notifier` จากภายนอกไว้ และหลีกเลี่ยงการสร้าง concrete notifier ภายใน `InventoryService` |

