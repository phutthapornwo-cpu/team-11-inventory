# Debugging & Root Cause Analysis Log - discount.py

## 1. จุดที่พบ Bug และ Root Cause Analysis

1. **`apply_discount()` - Mathematical Logic Bug:**
   - **สาเหตุ:** คำนวณส่วนลดผิดสูตรเป็น `price - percent / 100` ทำให้ส่วนลดคิดเป็นค่าคงที่ ไม่ได้คิดตามเปอร์เซ็นต์ของราคาสินค้า
   - **การแก้ไข:** เปลี่ยนสูตรคำนวณเป็น `price - (price * percent / 100)` พร้อมเพิ่มการตรวจจับค่าติดลบ/ค่าเกิน 100%

2. **`cheapest_n()` - Array Off-by-one Error:**
   - **สาเหตุ:** ใช้ Slicing `ordered[1:n]` ซึ่งทำให้ข้ามสินค้าที่ราคาถูกที่สุด (Index 0) ไป และคืนจำนวนรายการไม่ครบตาม $n$
   - **การแก้ไข:** แก้เป็น `ordered[:n]` เพื่อเริ่มตัดจากอินเด็กซ์ตัวแรกสุด

3. **`average_price()` - ZeroDivisionError:**
   - **สาเหตุ:** เกิด crash ทันทีหากส่ง array ว่าง `[]` เข้ามา เนื่องจากตัวหาร `len(prices)` เป็น 0
   - **การแก้ไข:** เพิ่ม Guard Clause `if not prices: return 0.0`

## 2. ผลการรัน Unit Test หลังแก้ไข
รันคำสั่ง `pytest tests/test_discount.py` ผ่านทั้งหมด **100% (Passed)**