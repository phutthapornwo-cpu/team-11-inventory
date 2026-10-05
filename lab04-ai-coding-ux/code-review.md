# Code Review Report - AI Generated Code

## รายละเอียด Pull Request
- **PR Title:** Feature/Add discount and stock reduction module
- **Reviewer:** [ใส่ชื่อ-นามสกุล หรือ รหัสนักศึกษาของคุณ]
- **Source Code:** โค้ดโมดูลคำนวณส่วนลดและการตัดสต็อกสินค้าที่สร้างโดย AI

---

## 1. ภาพรวมการรีวิว (Executive Summary)
จากการรีวิวโค้ดที่ AI เจนเนอเรต พบว่าโค้ดทำงานได้ตามโจทย์พื้นฐาน (Happy Path) แต่ยังพบ **Bug แฝง**, **ข้อผิดพลาดทาง Security**, และ **Edge Cases ที่ยังไม่ได้รับการจัดการ** ซึ่งจำเป็นต้องได้รับการแก้ไขก่อนทำการ Merge เข้าสู่ Branch หลัก

---

## 2. รายการข้อผิดพลาดที่พบ (Review Findings)

| ลำดับ | ประเภทปัญหา | รายละเอียดปัญหา / ตำแหน่งที่พบ | ผลกระทบที่อาจเกิดขึ้น | แนวทางการแก้ไข |
|---|---|---|---|---|
| 1 | **Business Logic / Edge Case** | ไม่เช็กจำนวนสินค้าสั่งซื้อเป็น 0 หรือติดลบ ในฟังก์ชันตัดสต็อก | สต็อกสินค้าอาจเพิ่มขึ้นเองได้หากใส่จำนวนติดลบ (`stock - (-5) = stock + 5`) | ใส่ Validation ตรวจสอบ `if quantity <= 0:` แล้ว raise `ValueError` |
| 2 | **Security Issue** | มีการใช้ `eval()` หรือสั่ง Execute Query ตรงๆ โดยไม่ผ่าน Parameterized Query | เสี่ยงต่อการเกิด SQL Injection หรือ Remote Code Execution (RCE) | เปลี่ยนมาใช้ Parameterized Queries (`?` หรือ `%s`) |
| 3 | **Data Integrity** | ไม่ตรวจสอบความคงเส้นคงวาของประเภทข้อมูล (Type Mismatch) เช่น ส่ง `quantity` เป็น String `"5"` เข้ามา | ทำให้การคำนวณผิดพลาดหรือโปรแกรม crash (`TypeError`) | ใช้ Type Casting / Type Hints หรือการตรวจ validation `isinstance()` |
| 4 | **Logic Bug (Floating Point)** | ใช้การคำนวณราคาและส่วนลดแบบ `float` โดยตรง เช่น `price * 0.1` | เกิดปัญหาความคลาดเคลื่อนของทศนิยม (Floating point inaccuracy) | เปลี่ยนมาใช้โมดูล `decimal.Decimal` หรือปัดเศษทศนิยมให้ถูกต้องด้วย `round()` |
| 5 | **Error Handling** | ใช้ `except Exception:` แบบครอบจักรวาล โดยไม่มีการบันทึก Log หรือจัดการเฉพาะประเภท Error | สยบ Error ไว้เงียบๆ ทำให้ผู้ใช้ไม่รู้ว่าเกิดอะไรขึ้น และหา Root cause ยาก | แยกประเภท Exception เช่น `ValueError`, `KeyError` และส่ง Message แจ้งเตือนชัดเจน |

---

## 3. ตัวอย่างการแก้ Code (Diff Comparison)

### จุดที่ 1: การป้องกันการตัดสต็อกด้วยจำนวนที่ติดลบ (Logic Bug)

#### Before (AI Generated Code):
```python
def deduct_stock(product, quantity):
    # AI ไม่ได้เช็กว่า quantity ติดลบหรือไม่
    product['stock'] -= quantity
    return product['stock']
```

#### After (Reviewed & Fixed):
```python
def deduct_stock(product: dict, quantity: int) -> int:
    if quantity <= 0:
        raise ValueError("จำนวนสินค้าที่ต้องการตัดต้องมากกว่า 0")
    
    if product.get('stock', 0) < quantity:
        raise ValueError("จำนวนสินค้าในคลังไม่พอ")
        
    product['stock'] -= quantity
    return product['stock']
```

---

## 4. ข้อเสนอแนะเพิ่มเติมสำหรับทีม
- **อย่าเชื่อโค้ด AI 100%:** AI มักจะเน้นทำให้โค้ดรันผ่านในเคสปกติ แต่มักจะมองข้าม Edge Cases และการจัดการ Exception
- **ต้องเขียน Unit Test กำกับเสมอ:** โดยเฉพาะการทดสอบ Boundary Values (เช่น ค่า 0, ค่าติดลบ, ค่าสูงสุด) เพื่อดักจับพฤติกรรมแปลกๆ ที่ AI สร้างไว้