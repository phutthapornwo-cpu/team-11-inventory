from __future__ import annotations

import json
from pathlib import Path

# ข้อมูล inventory แบบ persistence
items: dict[str, dict] = {}


def load_items(file_path: str | Path = "inventory.json") -> dict:
    """โหลดข้อมูลสินค้าจากไฟล์ JSON

    ถ้าไฟล์ไม่มีอยู่ จะคืนค่าเป็น dictionary ว่าง
    """
    path = Path(file_path)

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_items(
    data: dict | None = None,
    file_path: str | Path = "inventory.json",
) -> None:
    """บันทึกข้อมูลสินค้าลงไฟล์ JSON"""
    data = items if data is None else data

    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def add_item(code: str, name: str, quantity: int) -> str:
    """เพิ่มสินค้าใหม่เข้าสู่ inventory"""
    global items

    if quantity < 0:
        return "จำนวนสินค้าต้องไม่ติดลบ"

    if code in items:
        return "รหัสสินค้าซ้ำ"

    items[code] = {
        "name": name,
        "quantity": quantity,
    }

    save_items(items)

    return "เพิ่มสินค้าสำเร็จ"


class Inventory:
    def __init__(self, items=None):
        """เก็บข้อมูลสินค้าในคลัง

        รองรับทั้ง Dict, Dict of Dicts และ List of Dicts
        """
        if items is None:
            self.items = {}
        else:
            self.items = items

    def add_item(self, name, quantity):
        """เพิ่มหรืออัปเดตจำนวนสินค้า"""
        if isinstance(self.items, dict):
            if name in self.items and isinstance(self.items[name], dict):
                self.items[name]["quantity"] = (
                    self.items[name].get("quantity", 0) + quantity
                )
            else:
                self.items[name] = self.items.get(name, 0) + quantity

    def low_stock_items(self, threshold):
        """ส่งคืนรายการสินค้าที่มีจำนวน <= threshold"""
        result = []

        if isinstance(self.items, dict):
            for name, data in self.items.items():
                if isinstance(data, dict):
                    qty = data.get("quantity", 0)
                else:
                    qty = data

                if qty <= threshold:
                    result.append(name)

        elif isinstance(self.items, list):
            for item in self.items:
                if isinstance(item, dict):
                    name = item.get("name")
                    qty = item.get("quantity", 0)

                    if qty <= threshold:
                        result.append(name)

        return sorted(result)

    def sell(self, name, quantity):
        """ตัดสต็อกสินค้าเมื่อทำการขาย"""
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if isinstance(self.items, dict):
            if name not in self.items:
                raise KeyError(f"Item '{name}' not found in inventory")

            if isinstance(self.items[name], dict):
                current_qty = self.items[name]["quantity"]
            else:
                current_qty = self.items[name]

            if quantity <= 0:
                raise ValueError("Quantity to sell must be greater than zero")

            if current_qty < quantity:
                raise ValueError(f"Insufficient stock for '{name}'")

            if isinstance(self.items[name], dict):
                self.items[name]["quantity"] -= quantity
            else:
                self.items[name] -= quantity