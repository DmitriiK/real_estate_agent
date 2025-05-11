import unittest
from datetime import datetime
from decimal import Decimal
from src.utils.utils import make_json_serializable

class TestMakeJsonSerializable(unittest.TestCase):

    def test_make_json_serializable(self):
        data = [
            {"id": 1, "price": Decimal("1234.5678"), "created_at": datetime(2025, 5, 11, 15, 30, 45)},
            {"id": 2, "price": Decimal("9876.5432"), "created_at": datetime(2025, 5, 10, 12, 15, 0)},
        ]

        make_json_serializable(data)

        expected = [
            {"id": 1, "price": 1234.57, "created_at": "2025-05-11"},
            {"id": 2, "price": 9876.54, "created_at": "2025-05-10"},
        ]

        self.assertEqual(data, expected)

if __name__ == "__main__":
    unittest.main()