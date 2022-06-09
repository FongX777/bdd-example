import unittest
from typing import List


class Product:
    def __init__(self, name: str, unit_price: int, max_purchase_quantity: int):
        self.name = name
        self.unit_price = unit_price
        self.max_purchase_quantity = max_purchase_quantity


class CartItem:
    def __init__(self, quantity: int, product: Product):
        self.quantity = quantity
        self.product = product


class Cart:
    shipping_fee = 60

    def __init__(self, cart_items: List[CartItem] = None):
        self.cart_items = [] if cart_items is None else cart_items

    def add(self, item: CartItem):
        self.cart_items.append(item)
        return sum(cart_item.product.unit_price * cart_item.quantity
                   for cart_item in self.cart_items) + self.shipping_fee


class TestWhenAddingItemToCart(unittest.TestCase):
    def test_total_should_be_the_sum_up_subtotals_of_all_items_plus_shipping_fee(
            self):
        # given
        cart = Cart([
            CartItem(
                5,
                Product(name='Eraser', unit_price=10,
                        max_purchase_quantity=10))
        ])

        # when
        price = cart.add(
            CartItem(
                10,
                Product(name='Pencil', unit_price=20,
                        max_purchase_quantity=10)))

        # then
        self.assertEqual(price, 310)
