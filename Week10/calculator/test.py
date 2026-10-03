import unittest
import calculator

class TestCalculator(unittest.TestCase):

    def test_add(self):
        result = calculator.add(2, 3)
        self.assertEqual(result, 5)

    def test_divide(self):
        result = calculator.divide(10, 2)
        self.assertAlmostEqual(result, 5)

    def test_multiply(self):
        result = calculator.multiply(5, 7)
        self.assertEqual(result, 35)

    def test_minus(self):
        result = calculator.minus(23, 8)
        self.assertEqual(result, 15)

    def test_power(self):
        result = calculator.power(2, 3)
        self.assertEqual(result, 8)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(10, 0)

if __name__ == '__main__':
    unittest.main()