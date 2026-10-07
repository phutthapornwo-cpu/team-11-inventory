# บันทึก Test Gap จากการให้ AI เขียน Unit Test (ขั้นที่ 4)

| กรณีที่ AI ให้มา (Happy Path) | กรณีที่ AI ขาดไป (Edge Case / Error) | Test ที่เราเขียนเสริม |
| :--- | :--- | :--- |
| ขายสินค้าจำนวนปกติเมื่อมี stock พอ | ขายหมดพอดีจนเหลือ 0 ชิ้น | `test_sell_exact_remaining` |
| | ขายจำนวน 0 ชิ้น หรือ ขายจำนวนติดลบ | `test_sell_zero_or_negative` |
| | ขายสินค้ามากกว่าจำนวนที่มีอยู่ในคลัง | `test_sell_exceeds_stock` |
| | ขายสินค้าที่ไม่มีอยู่ในระบบ | `test_sell_non_existent_item` |
| | ใส่จำนวนสินค้าเป็นชนิดข้อมูลผิด (String/Float) | `test_sell_invalid_type` |