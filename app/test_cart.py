import unittest
from typing import List

import pytest


class Product:
    def __init__(self, name: str, unit_price: int, max_purchase_quantity: int):
        self.name = name
        self.unit_price = unit_price
        self.max_purchase_quantity = max_purchase_quantity


class CartItem:
    def __init__(self, quantity: int, product: Product):
        if quantity > product.max_purchase_quantity:
            raise ValueError(
                f'already reach the maximum purchase quantity of {product.name}: {product.max_purchase_quantity}')

        self.quantity = quantity
        self.product = product

    def add_quantity(self, quantity: int):
        return CartItem(self.quantity + quantity, self.product)

    @property
    def subtotal(self):
        return self.product.unit_price * self.quantity


class Cart:
    shipping_fee = 60

    def __init__(self, cart_items: List[CartItem] = None):
        self.cart_items = [] if cart_items is None else cart_items

    def add(self, item: CartItem):
        index = next((i for i, it in enumerate(self.cart_items) if it.product.name == item.product.name), -1)
        if index >= 0:
            self.cart_items[index] = self.cart_items[index].add_quantity(item.quantity)
        else:
            self.cart_items.append(item)

        return sum(cart_item.subtotal for cart_item in self.cart_items) + self.shipping_fee


class TestWhenAddingItemToCart(unittest.TestCase):
    def setUp(self):
        self.product_pencil = Product(name='Pencil', unit_price=20, max_purchase_quantity=10)
        self.product_eraser = Product(name='Eraser', unit_price=10, max_purchase_quantity=10)

    def test_total_should_be_the_sum_up_subtotals_of_all_items_plus_shipping_fee(self):
        # given
        cart = Cart([CartItem(5, self.product_eraser)])

        # when
        price = cart.add(CartItem(10, self.product_pencil))

        # then
        self.assertEqual(price, 310)

    def test_should_show_error_when_add_to_existing_items_that_is_more_tha_the_product_max_purchase_qty(self):
        # given
        cart = Cart([CartItem(10, self.product_eraser)])

        # when
        with pytest.raises(ValueError) as e:
            cart.add(CartItem(1, self.product_eraser))

        # then
        self.assertTrue('already reach the maximum purchase quantity of Eraser: 10' in str(e.value))

    def test_should_show_error_when_add_new_items_with_too_many_qty(self):
        # given
        cart = Cart()

        # when
        with pytest.raises(ValueError) as e:
            cart.add(CartItem(11, self.product_eraser))

        # then
        self.assertTrue('already reach the maximum purchase quantity of Eraser: 10' in str(e.value))


class CartItemTest(unittest.TestCase):
    def test_quantity_should_not_surpass_product_maximum_purchase_qty(self):
        with pytest.raises(ValueError) as e:
            Cart([CartItem(11, Product('Pencil', 20, 10))])
        self.assertEqual('already reach the maximum purchase quantity of Pencil: 10', str(e.value))
