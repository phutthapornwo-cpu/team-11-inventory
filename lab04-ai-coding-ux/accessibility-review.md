echo # Accessibility Review - Lab 04 > lab04-ai-coding-ux\accessibility-review.md
echo. >> lab04-ai-coding-ux\accessibility-review.md
echo ^| รายการตรวจ ^| ผ่าน หรือ ไม่ผ่าน ^| สิ่งที่แก้ ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| --- ^| --- ^| --- ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ข้อความหลักบนพื้นขาว contrast อย่างน้อย 4.5 ต่อ 1 ^| ผ่าน ^| เลือกใช้สีข้อความ #111827 บนพื้นขาว ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ปุ่มหลักมี contrast เพียงพอ ^| ผ่าน ^| ใช้ปุ่มสี Primary #1E40AF กับตัวอักษรสีขาว ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ทุกช่องกรอกมี label ที่มองเห็น ^| ผ่าน ^| ย้ายข้อความจาก placeholder มาเป็น Visible Label ด้านบน ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ช่องที่บังคับกรอกมีสัญลักษณ์ชัด ^| ผ่าน ^| ใส่เครื่องหมาย * สีแดงกำกับท้าย Label ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| error ไม่ได้ใช้สีอย่างเดียว มีไอคอนหรือข้อความด้วย ^| ผ่าน ^| เพิ่มไอคอน [!] และข้อความอธิบายวิธีแก้ปัญหา ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ลำดับการกด Tab เรียงบนลงล่าง ซ้ายไปขวา ^| ผ่าน ^| จัดโครงสร้าง HTML/DOM ตามลำดับการอ่าน ^| >> lab04-ai-coding-ux\accessibility-review.md
echo ^| ปุ่มมีชื่อบอกหน้าที่ ไม่ใช่ OK หรือกากบาท ^| ผ่าน ^| เปลี่ยนเป็น "เข้าสู่ระบบ", "บันทึกสินค้า", "ยกเลิก" ^| >> lab04-ai-coding-ux\accessibility-review.md
echo. >> lab04-ai-coding-ux\accessibility-review.md
echo ## จุดที่ AI ทำพลาดแล้วเราปรับแก้เอง (อย่างน้อย 2 จุด): >> lab04-ai-coding-ux\accessibility-review.md
echo 1. **การใช้ Placeholder แทน Label:** AI มักสร้างฟิลด์กรอกข้อมูลโดยใส่แค่ placeholder ซึ่งจะหายไปเมื่อผู้ใช้พิมพ์ ทำให้จำไม่ได้ว่าฟิลด์นั้นคืออะไร -> **แก้โดย:** เพิ่ม Visible Label กำกับไว้ด้านบนทุกฟิลด์ >> lab04-ai-coding-ux\accessibility-review.md
echo 2. **Error State ใช้แค่สี:** AI สร้างข้อความแจ้งเตือนด้วยการเปลี่ยนสีขอบเป็นสีแดงอย่างเดียว ซึ่งผู้บกพร่องทางการมองเห็นสีจะสังเกตไม่ออก -> **แก้โดย:** เพิ่มไอคอน [!] และข้อความอธิบายวิธีแก้ไขปัญหากำกับไว้ใต้ฟิลด์ >> lab04-ai-coding-ux\accessibility-review.md