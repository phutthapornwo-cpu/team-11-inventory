import tempfile
import unittest
from pathlib import Path

from inventory import load_items, save_items


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


if __name__ == "__main__":
    unittest.main()
