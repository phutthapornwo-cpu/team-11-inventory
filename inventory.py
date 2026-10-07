class Inventory:
    def __init__(self, items=None):
        """
        เก็บข้อมูลสินค้าในคลัง
        รองรับทั้ง Dict, Dict of Dicts, และ List of Dicts
        """
        if items is None:
            self.items = {}
        else:
            self.items = items

    def add_item(self, name, quantity):
        """เพิ่มหรืออัปเดตจำนวนสินค้า"""
        if isinstance(self.items, dict):
            if name in self.items and isinstance(self.items[name], dict):
                self.items[name]['quantity'] = self.items[name].get('quantity', 0) + quantity
            else:
                self.items[name] = self.items.get(name, 0) + quantity

    def low_stock_items(self, threshold):
        """
        ส่งคืนรายการสินค้าที่มีจำนวนน้อยกว่าหรือเท่ากับ threshold
        โดยเรียงลำดับผลลัพธ์ตามชื่อสินค้า
        """
        result = []

        if isinstance(self.items, dict):
            for name, data in self.items.items():
                if isinstance(data, dict):
                    qty = data.get('quantity', 0)
                else:
                    qty = data
                
                if qty <= threshold:
                    result.append(name)

        elif isinstance(self.items, list):
            for item in self.items:
                if isinstance(item, dict):
                    name = item.get('name')
                    qty = item.get('quantity', 0)
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

            # ดึงจำนวนปัจจุบัน
            current_qty = self.items[name]['quantity'] if isinstance(self.items[name], dict) else self.items[name]

            if quantity <= 0:
                raise ValueError("Quantity to sell must be greater than zero")
            if current_qty < quantity:
                raise ValueError(f"Insufficient stock for '{name}'")

            # ตัดสต็อก
            if isinstance(self.items[name], dict):
                self.items[name]['quantity'] -= quantity
            else:
                self.items[name] -= quantity