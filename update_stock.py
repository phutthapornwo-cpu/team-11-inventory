# สมมติโครงสร้างข้อมูลสต็อกสินค้า
# key = รหัสสินค้า (code), value = จำนวนคงเหลือ (quantity)
inventory = {
    "P001": 50,
    "P002": 20,
}

def update_stock(code: str, action: str, amount: int):
    """
    อัปเดตยอดคงเหลือของสินค้า
    :param code: รหัสสินค้า
    :param action: 'in' (รับเข้า) หรือ 'out' (จ่ายออก)
    :param amount: จำนวนที่ต้องการรับเข้า/จ่ายออก
    :return: dict ผลลัพธ์ {success, message, new_balance}
    """

    # 1) Validate: amount ต้องเป็นจำนวนบวก
    if amount <= 0:
        return {
            "success": False,
            "message": "จำนวนต้องมากกว่า 0",
            "new_balance": None
        }

    # 2) Validate: ต้องมีรหัสสินค้านี้ในระบบ
    if code not in inventory:
        return {
            "success": False,
            "message": f"ไม่พบสินค้ารหัส {code} ในระบบ",
            "new_balance": None
        }

    current_balance = inventory[code]

    # 3) Logic คำนวณตาม action
    if action == "in":
        new_balance = current_balance + amount

    elif action == "out":
        # 4) Validate: ห้ามจ่ายออกเกินยอดคงเหลือ
        if amount > current_balance:
            return {
                "success": False,
                "message": "จำนวนคงเหลือไม่พอ",
                "new_balance": current_balance  # ยอดเดิม ไม่แก้ไข
            }
        new_balance = current_balance - amount

    else:
        # กัน action ที่ไม่ใช่ 'in'/'out'
        return {
            "success": False,
            "message": "action ไม่ถูกต้อง (ต้องเป็น 'in' หรือ 'out')",
            "new_balance": None
        }

    # 5) ถ้าผ่านทุกเงื่อนไข -> อัปเดตยอดจริง
    inventory[code] = new_balance

    return {
        "success": True,
        "message": "อัปเดตสต็อกสำเร็จ",
        "new_balance": new_balance
    }