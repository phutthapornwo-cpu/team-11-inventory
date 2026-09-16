sequenceDiagram
    autonumber
    actor Staff as พนักงานคลังสินค้า
    participant IS as InventoryService
    participant P as Product
    participant ST as StockTransaction
    participant N as Notifier (Email/SMS)

    Staff->>IS: issue_stock(product_id, quantity)
    activate IS
    
    IS->>IS: ตรวจสอบ validation (quantity > 0, product_id มีอยู่จริง)
    
    alt สินค้าไม่มีในระบบ หรือ quantity <= 0
        IS-->>Staff: Raise ValueError
    end

    IS->>P: ดึงข้อมูลสินค้าและตรวจสต็อก (product.quantity)
    activate P
    P-->>IS: คืนค่าสต็อกปัจจุบัน
    deactivate P

    alt quantity > product.quantity
        IS-->>Staff: Raise ValueError ("สต็อกไม่เพียงพอ")
    end

    Note over IS,P: คำนวณสต็อกใหม่<br/>stock_after = product.quantity - quantity
    IS->>P: อัปเดต stockคงเหลือ (product.quantity = stock_after)
    
    create participant ST
    IS->>ST: บันทึกประวัติการจ่ายสินค้า (StockTransaction)
    
    IS->>IS: ตรวจสอบเงื่อนไข (product.quantity <= product.threshold)

    opt สต็อกต่ำกว่าหรือเท่ากับ threshold
        IS->>IS: _notify_low_stock(product)
        loop สำหรับทุก Notifier ใน self.notifiers
            IS->>N: send(message)
            activate N
            Note over N: แสดงผลข้อความแจ้งเตือน (Mock)
            N-->>IS: ดำเนินการสำเร็จ / ส่งผลลัพธ์
            deactivate N
        end
    end

    IS-->>Staff: คืนค่า StockTransaction
    deactivate IS