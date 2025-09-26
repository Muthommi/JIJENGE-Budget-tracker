import unittest
from jijenge_core.fees.calculator import FeeCalculator

class TestFeeCalculator(unittest.Testcase):
    def setUp(self):
        self.fc = FeeCalculator()

    def test_p2p_band(self):
        self.assertEqual(self.fc.calc_fee(50, "p2p"), 0.0)
        self.assertEqual(self.fc.calc_fee(200, "p2p"), 12.0)
        self.assertEqual(self.fc.calc_fee(800, "p2p"), 15.0)

    def test_paybill(self):
        self.assertEqual(self.fc.calc_fee(100, "paybill"), 12.0)
        self.assertEqual(self.fc.calc_fee(700, "paybill"), 15.0)

    def test_till(self):
        self.assertEqual(self.fc.calc_fee(5000, "till"), 0.0)


if __name__ == '__main__':
    unittest.main
