import unittest
from unittest.mock import patch
from shop import Inventory, OutOfStockError, Product, calculate_price
from tax import total_with_tax
class TestCalculatePrice(unittest.TestCase):
    def test_basic_price(self):
        self.assertEqual(calculate_price(60, 3), 180)
 
    def test_discount_applied(self):
        self.assertAlmostEqual(calculate_price(60, 3, 0.1), 162.0, places=2)
    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError):
            calculate_price(60, 0)
    def test_bad_prices_rejected(self):
        for price in (0, -5):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    calculate_price(price, 1)
class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Keyboard", 60.0, stock=3)
    def test_new_product_is_in_stock(self):
        self.assertTrue(self.product.in_stock)
    def test_sell_reduces_stock(self):
        self.product.sell(2)
        self.assertEqual(self.product.stock, 1)
    def test_selling_too_many_raises(self):
        with self.assertRaises(OutOfStockError) as ctx:
            self.product.sell(4)
        self.assertIn("Keyboard", str(ctx.exception))
    def test_restock_adds_stock(self):
        self.product.restock(5)
        self.assertEqual(self.product.stock, 8)
    @unittest.skip("gift wrapping is not built yet")
    def test_gift_wrap(self):
        pass
class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.keyboard = Product("Keyboard", 60.0, stock=3)
        self.mouse = Product("Mouse", 15.0, stock=5)
        self.inventory.add(self.keyboard)
        self.inventory.add(self.mouse)
    def test_cheapest_in_stock(self):
        self.assertIs(self.inventory.cheapest_in_stock(), self.mouse)
    def test_cheapest_skips_sold_out_products(self):
        self.mouse.sell(5)
        self.assertIs(self.inventory.cheapest_in_stock(), self.keyboard)
    def test_none_when_everything_is_sold_out(self):
        self.mouse.sell(5)
        self.keyboard.sell(3)
        self.assertIsNone(self.inventory.cheapest_in_stock())
class TestTax(unittest.TestCase):
    @patch("tax.get_tax_rate", return_value=0.15)
    def test_total_with_tax(self, mock_rate):
        self.assertEqual(total_with_tax(60, 3), 207.0)
        mock_rate.assert_called_once()
    def test_service_down_is_propagated(self):
        with patch("tax.get_tax_rate", side_effect=RuntimeError("down")):
            with self.assertRaises(RuntimeError):
                total_with_tax(60, 3)
if __name__ == "__main__":
    unittest.main()