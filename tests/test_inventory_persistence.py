import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import inventory
from inventory import add_item, load_items, save_items


class TestInventoryPersistence(unittest.TestCase):
    def test_load_items_returns_empty_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "missing.json"
            self.assertEqual(load_items(file_path), {})

    def test_save_and_load_items_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "items.json"
            sample_items = {
                "P001": {"name": "Laptop", "quantity": 3},
                "P002": {"name": "Mouse", "quantity": 10},
            }

            save_items(sample_items, file_path)
            loaded_items = load_items(file_path)

            self.assertEqual(loaded_items, sample_items)


class TestAddItem(unittest.TestCase):
    def setUp(self):
        inventory.items = {}

    def test_add_item_success(self):
        with patch("inventory.save_items") as mock_save_items:
            result = add_item("P001", "Laptop", 5)

        self.assertEqual(result, "เพิ่มสินค้าสำเร็จ")
        self.assertEqual(
            inventory.items["P001"],
            {"name": "Laptop", "quantity": 5}
        )
        mock_save_items.assert_called_once_with(inventory.items)

    def test_add_item_allows_zero_initial_stock(self):
        with patch("inventory.save_items") as mock_save_items:
            result = add_item("P002", "Mouse", 0)

        self.assertEqual(result, "เพิ่มสินค้าสำเร็จ")
        self.assertEqual(inventory.items["P002"]["quantity"], 0)
        mock_save_items.assert_called_once_with(inventory.items)

    def test_add_item_duplicate_code_rejected_without_data_change(self):
        inventory.items = {"P001": {"name": "Laptop", "quantity": 3}}
        before_items = inventory.items.copy()

        with patch("inventory.save_items") as mock_save_items:
            result = add_item("P001", "Keyboard", 10)

        self.assertEqual(result, "รหัสสินค้าซ้ำ")
        self.assertEqual(inventory.items, before_items)
        mock_save_items.assert_not_called()

    def test_add_item_negative_stock_rejected_without_data_change(self):
        with patch("inventory.save_items") as mock_save_items:
            result = add_item("P003", "Tablet", -1)

        self.assertEqual(result, "จำนวนสินค้าต้องไม่ติดลบ")
        self.assertNotIn("P003", inventory.items)
        mock_save_items.assert_not_called()


if __name__ == "__main__":
    unittest.main()
