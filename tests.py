import unittest
from feiertagsrechner import get_params

class TestGetParams(unittest.TestCase):
    def test_get_params(self):
        # Test with valid input
        params = get_params(2022, "BW", "rk", False, False, False, 3)
        self.assertEqual(params["year"], 2022)
        self.assertEqual(params["state"], "BW")
        self.assertEqual(params["confession"], "rk")
        self.assertEqual(params["augsburg"], False)
        self.assertEqual(params["fronleichnamSachsen"], False)
        self.assertEqual(params["fronleichnamThueringen"], False)
        self.assertEqual(params["days"], [0, 1, 2])

        # Test with invalid input
        with self.assertRaises(ValueError):
            get_params(2022, "XX", "rk", False, False, False, 3)

if __name__ == '__main__':
    unittest.main()