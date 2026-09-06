import json
from pathlib import Path

# เก็บข้อมูลสินค้าในระบบ
DATA_FILE = Path("items.json")
items = {}


def load_items(file_path=DATA_FILE):
    """อ่านข้อมูลสินค้าจากไฟล์ JSON"""
    path = Path(file_path)
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

    return data if isinstance(data, dict) else {}


def save_items(items_data, file_path=DATA_FILE):
    """บันทึกข้อมูลสินค้าลงไฟล์ JSON"""
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(items_data, file, ensure_ascii=False, indent=2)


def add_item(code, name, initial_stock):
    """เพิ่มสินค้าใหม่เข้าระบบพร้อมตรวจสอบข้อมูล"""
    if code in items:
        return "รหัสสินค้าซ้ำ"

    if initial_stock < 0:
        return "จำนวนสินค้าต้องไม่ติดลบ"

    items[code] = {
        "name": name,
        "quantity": initial_stock
    }
    save_items(items)
    return "เพิ่มสินค้าสำเร็จ"


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


def update_stock(item_id, qty_change):
    """
    ปรับยอดคงเหลือของสินค้า (Task 2: Immediate Persistence)
    qty_change: บวก = รับเข้า, ลบ = จ่ายออก
    คืนค่า (success: bool, message: str, new_qty: int หรือ None)
    """
    # AC: ต้องมีสินค้ารหัสนี้อยู่ในระบบก่อน
    if item_id not in items:
        return False, "ไม่พบรหัสสินค้านี้ในระบบ", None

    current_qty = items[item_id]["quantity"]
    new_qty = current_qty + qty_change

    # AC-2: ถ้าจ่ายออกมากกว่าคงเหลือ ห้ามอัปเดต/บันทึกไฟล์ ยอดคงเหลือต้องไม่เปลี่ยน
    if new_qty < 0:
        return False, "จำนวนคงเหลือไม่พอ", None

    # AC-1: ถ้าผ่านเงื่อนไข ให้อัปเดตค่าและบันทึกไฟล์ทันที
    items[item_id]["quantity"] = new_qty
    save_items(items)
    return True, "อัปเดตสต็อกสำเร็จ", new_qty


def main_menu():
    """รับข้อมูลสินค้าจาก Terminal และจัดการเมนูหลัก"""
    global items
    items = load_items()

    while True:
        print("\n=== ระบบจัดการสินค้า ===")
        print("1. เพิ่มสินค้า")
        print("2. แสดงรายการสินค้าทั้งหมด")
        print("3. รับเข้า/จ่ายออกสินค้า")
        print("4. ออกจากระบบ")

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
            except ValueError:
                print("กรุณากรอกจำนวนสินค้าเป็นตัวเลขเท่านั้น")
                continue

            print(add_item(product_id, product_name, quantity))

        elif choice == "2":
            list_items()

        elif choice == "3":
            # Task 3: เมนูรับเข้า/จ่ายออกสินค้าผ่าน CLI
            product_id = input("กรอกรหัสสินค้า: ").strip()

            if product_id not in items:
                print("ไม่พบรหัสสินค้านี้ในระบบ")
                continue

            action = input("ประเภทรายการ (in = รับเข้า / out = จ่ายออก): ").strip().lower()
            if action not in ("in", "out"):
                print("กรุณาเลือก in หรือ out เท่านั้น")
                continue

            try:
                quantity = int(input("กรอกจำนวน: "))
            except ValueError:
                print("กรุณากรอกจำนวนเป็นตัวเลขเท่านั้น")
                continue

            if quantity < 0:
                print("จำนวนต้องไม่ติดลบ")
                continue

            qty_change = quantity if action == "in" else -quantity
            success, message, new_qty = update_stock(product_id, qty_change)

            if success:
                print(f"{message} ยอดคงเหลือใหม่: {new_qty}")
            else:
                print(message)

        elif choice == "4":
            print("ออกจากระบบ")
            break

        else:
            print("กรุณาเลือกเมนู 1, 2, 3 หรือ 4")


if __name__ == "__main__":
    main_menu()