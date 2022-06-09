import unittest

import pytest

from app.archive2.cart import BundleDiscount, Cart, CartItem, Product, \
    QtyDiscount


class TestCartCalculation(unittest.TestCase):
    def test_total_should_be_the_sum_of_subtotal(self):
        cart = Cart()
        cart_items = [
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=10),
            CartItem(Product(name='Eraser', price=30, max_purchase_qty=10),
                     qty=10),
        ]
        price = cart.calculate(cart_items)
        self.assertEqual(price, 500)

    def test_should_fail_when_cart_has_over_5_items(self):
        cart = Cart()
        cart_items = [
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=10),
            CartItem(Product(name='Eraser', price=30, max_purchase_qty=10),
                     qty=10),
            CartItem(Product(name='Blue Pen', price=30, max_purchase_qty=10),
                     qty=10),
            CartItem(Product(name='X', price=30, max_purchase_qty=10), qty=10),
            CartItem(Product(name='Y', price=30, max_purchase_qty=10), qty=10),
            CartItem(Product(name='Z', price=30, max_purchase_qty=10), qty=10),
        ]
        with pytest.raises(ValueError) as e:
            cart.calculate(cart_items)
        self.assertTrue('Cart cannot have more than 5 items' in str(e))

    def test_should_discount_when_qty_discount_applied(self):
        discount = QtyDiscount(product_name='Pencil',
                               qty=2,
                               discount_percentage_off=10)
        cart = Cart(discounts=[discount])
        cart_items = [
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=2),
        ]
        price = cart.calculate(cart_items)
        self.assertEqual(price, 36)

    def test_should_discount_when_same_qty_discount_applied_multiple_times(
            self):
        discount = QtyDiscount(product_name='Pencil',
                               qty=2,
                               discount_percentage_off=10)
        cart = Cart(discounts=[discount])
        cart_items = [
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=4),
        ]
        price = cart.calculate(cart_items)
        self.assertEqual(price, 72)

    def test_should_discount_when_bundle_discount_applied(self):
        discount = BundleDiscount(product_a_name='Pencil',
                                  product_b_name='Eraser',
                                  deduction_amount=10)
        cart = Cart(discounts=[discount])
        cart_items = [
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=1),
            CartItem(Product(name='Eraser', price=30, max_purchase_qty=10),
                     qty=1),
        ]
        price = cart.calculate(cart_items)
        self.assertEqual(price, 40)


class WhenNewProduct(unittest.TestCase):
    # Question: 我應該要怎麼命名這一段？我想測試 0 & -1
    def test_should_fail_when_price_is_zero(self):
        with pytest.raises(ValueError):
            Product(name='Pencil', price=0, max_purchase_qty=10)

    def test_should_fail_when_price_is_negative(self):
        with pytest.raises(ValueError):
            Product(name='Pencil', price=-1, max_purchase_qty=10)


class TestNewCartItem(unittest.TestCase):
    def test_should_fail_when_qty_exceeds_product_max_purchase_qty(self):
        with pytest.raises(ValueError) as e:
            CartItem(Product(name='Pencil', price=20, max_purchase_qty=10),
                     qty=11)
        self.assertTrue('Cannot add more than 10 of Pencil' in str(e))
