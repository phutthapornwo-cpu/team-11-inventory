# Prompt Engineering & Context Engineering Comparison

## โจทย์ที่ใช้ทดสอบ
ต้องการสร้างฟังก์ชันลดจำนวนสินค้าในคลัง (Deduct Stock / Reduce Inventory) ที่รองรับทั้งสินค้าจับต้องได้ (Physical Product) และสินค้าดิจิทัล (Digital Product)

---

## 1. รอบที่ 1: Prompt สั้นๆ (ไม่มี Context)

### Prompt ที่ใช้:
> "เขียนฟังก์ชัน Python สำหรับลดสต็อกสินค้าในระบบ inventory หน่อย"

### Code ผลลัพธ์จาก AI:
```python
def reduce_stock(item, quantity):
    item['stock'] -= quantity
    return item
```

---

## 2. รอบที่ 2: Prompt + Context Engineering (แนบ Context ครบถ้วน)

### Prompt ที่ใช้:
> "ขอฟังก์ชัน reduce_stock(product, quantity) ภาษา Python สำหรับระบบ Inventory ตามเงื่อนไขดังนี้:
> **Context & Rules:** Structure ของ product เป็น dictionary มี key: id, name, type ('physical' หรือ 'digital'), และ stock (int)
> - ถ้า type เป็น 'digital' ให้ข้ามการตัดสต็อกแล้ว return True ได้ทันที (ถือว่ามีสต็อกไม่จำกัด)
> - ถ้า type เป็น 'physical':
>   - ถ้า quantity <= 0 ให้ raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
>   - ถ้า stock < quantity ให้ raise ValueError("สินค้าในคลังไม่พอ")
>   - ถ้าผ่าน ให้ลด stock ตาม quantity และ return True
> ขอโค้ดที่รัดกุม มี Type Hint และ Docstring ชัดเจน"

### Code ผลลัพธ์จาก AI:
```python
def reduce_stock(product: dict, quantity: int) -> bool:
    """
    ลดจำนวนสินค้าในคลังตามประเภทสินค้า
    
    :param product: dict ข้อมูลสินค้าประกอบด้วย id, name, type, stock
    :param quantity: จำนวนที่ต้องการลด
    :return: True หากดำเนินการสำเร็จ
    :raises ValueError: หากจำนวนไม่ถูกต้องหรือสินค้าไม่พอ
    """
    product_type = product.get('type', 'physical')
    
    # กรณีสินค้าดิจิทัล ไม่จำกัดจำนวนสต็อก
    if product_type == 'digital':
        return True
    
    # ตรวจสอบความถูกต้องของจำนวน
    if quantity <= 0:
        raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
        
    current_stock = product.get('stock', 0)
    if current_stock < quantity:
        raise ValueError("สินค้าในคลังไม่พอ")
        
    product['stock'] = current_stock - quantity
    return True
```

---

## 3. สรุปผลการเปรียบเทียบ

| หัวข้อการเปรียบเทียบ | รอบที่ 1: Prompt สั้นๆ (ไม่มี Context) | รอบที่ 2: Prompt + Context Engineering |
| :--- | :--- | :--- |
| **ความตรงตาม Requirement** | ไม่ตรง (เขียนแบบ Generic ไม่รองรับ Digital Product) | ตรงตาม Business Logic ทุกประการ |
| **ความรัดกุมของโค้ด** | ต่ำ (ไม่มี Validation/Error Handling) | สูง (มี Validation, Exception Handling, Type Hints) |
| **ความสะดวกในการนำไปใช้** | ต้องเสียเวลานำมาเขียนเพิ่มและแก้ไขเอง | พร้อมใช้งานได้ทันทีและนำไปทำ Unit Test ต่อได้ง่าย |
| **ระยะเวลาในการเตรียม Prompt** | สั้น สะดวกรวดเร็ว | ต้องใช้เวลาในการเรียบเรียง Requirement และ Context |

### สรุปข้อดี-ข้อเสีย

#### การทดสอบรอบที่ 1 (ไม่มี Context):
* **ข้อดี:** สะดวกรวดเร็วในการพิมพ์
* **ข้อเสีย:** โค้ดขาด Business Logic, ไม่มีการจัดการ Edge Case, ไม่ตรงตามโจทย์สินค้า Digital/Physical และไม่มี Error Handling

#### การทดสอบรอบที่ 2 (แนบ Context ครบถ้วน):
* **ข้อดี:**
  * โค้ดตรงตาม Business Logic ที่ระบบต้องการทันที
  * มี Edge Case Handling รัดกุม (ตรวจการติดลบ, สินค้าขาดตลาด)
  * แยกประเภทสินค้า Physical vs Digital ชัดเจนตามโจทย์
  * มี Type Hints และ Docstring ครอบคลุม ทำให้พร้อมนำไปพัฒนา Unit Test ต่อได้ง่าย
* **ข้อเสีย:** ต้องเสียเวลาเตรียม Prompt และเรียบเรียง Requirement ยาวกว่ารอบแรก