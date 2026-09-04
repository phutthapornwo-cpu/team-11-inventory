# เก็บข้อมูลสินค้าในระบบ
items = {}


def list_items():
    """แสดงรายการสินค้าทั้งหมดที่มีในระบบ (AC-1)"""
    if not items:
        print("ยังไม่มีสินค้าในระบบ")
        return

    print("\n=== รายการสินค้าทั้งหมด ===")
    for product_id, product in items.items():
        print(
            f"รหัส: {product_id}, "
            f"ชื่อ: {product['name']}, "
            f"จำนวนเริ่มต้น: {product['quantity']}"
        )


def main_menu():
    """รับข้อมูลสินค้าจาก Terminal และจัดการเมนูหลัก"""
    while True:
        print("\n=== ระบบจัดการสินค้า ===")
        print("1. เพิ่มสินค้า")
        print("2. แสดงรายการสินค้าทั้งหมด")
        print("3. ออกจากระบบ")

        choice = input("เลือกเมนู: ")

        if choice == "1":
            product_id = input("กรอกรหัสสินค้า: ").strip()
            product_name = input("กรอกชื่อสินค้า: ").strip()

            # ตรวจสอบรหัสสินค้าซ้ำ
            if product_id in items:
                print("รหัสสินค้าซ้ำ")
                continue

            try:
                quantity = int(input("กรอกจำนวนเริ่มต้น: "))

                if quantity < 0:
                    print("จำนวนสินค้าต้องไม่ติดลบ")
                    continue

            except ValueError:
                print("กรุณากรอกจำนวนสินค้าเป็นตัวเลขเท่านั้น")
                continue

            # เพิ่มสินค้าเข้าระบบ
            items[product_id] = {
                "name": product_name,
                "quantity": quantity
            }

            print("เพิ่มสินค้าสำเร็จ")

        elif choice == "2":
            list_items()

        elif choice == "3":
            print("ออกจากระบบ")
            break

        else:
            print("กรุณาเลือกเมนู 1, 2 หรือ 3")


if __name__ == "__main__":
    main_menu()
