import abc
import unittest
from typing import List, Optional

import pytest


class MemberService(abc.ABC):
    @abc.abstractmethod
    def query_is_member_vip(self) -> bool:
        pass


class FakeMemberService(MemberService):
    def __init__(self, is_vip: bool = False):
        self.is_vip = is_vip

    def query_is_member_vip(self) -> bool:
        return self.is_vip


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


class Discount(abc.ABC):
    @abc.abstractmethod
    def apply(self, cart_items: List[CartItem]) -> int:
        pass


class QuantityDiscount(Discount):
    def apply(self, cart_items: List[CartItem]) -> int:
        matched_item: Optional[CartItem] = next((it for it in cart_items if it.product.name == self.product_name), None)
        if not matched_item:
            return 0
        applied_times = int(matched_item.quantity / self.quantity)
        return int(applied_times * self.discount_percentage * self.quantity * matched_item.product.unit_price / 100)

    def __init__(self, name: str, product_name: str, quantity: int, discount_percentage: int):
        if discount_percentage not in [5, 10, 15]:
            raise ValueError(f'invalid discount percentage: {discount_percentage}')
        self.name = name
        self.product_name = product_name
        self.quantity = quantity
        self.discount_percentage = discount_percentage


class BundleDiscount(Discount):
    def apply(self, cart_items: List[CartItem]) -> int:
        matched_a: Optional[CartItem] = next((it for it in cart_items if it.product.name == self.product_a_name), None)
        matched_b: Optional[CartItem] = next((it for it in cart_items if it.product.name == self.product_b_name), None)

        if not matched_a or not matched_b:
            return 0

        applied_times = min(matched_a.quantity, matched_b.quantity)

        return int(applied_times * self.deduction_amount)

    def __init__(self, name: str, product_a_name: str, product_b_name: str, deduction_amount: int):
        if deduction_amount <= 0:
            raise ValueError(f'invalid deduction amount: {deduction_amount}')
        if product_a_name == product_b_name:
            raise ValueError(f'product a name cannot be the same as product b name: {product_a_name}')

        self.name = name
        self.product_a_name = product_a_name
        self.product_b_name = product_b_name
        self.deduction_amount = deduction_amount


class MemberServiceImpl(MemberService):
    def query_is_member_vip(self) -> bool:
        return False


class Cart:
    default_shipping_fee = 60

    def __init__(self,
                 cart_items: List[CartItem] = None,
                 discounts: List[Discount] = None,
                 member_service: MemberService = None):
        if cart_items is None:
            cart_items = []
        if discounts is None:
            discounts = []
        if member_service is None:
            member_service = MemberServiceImpl()
        self.cart_items = cart_items
        self.discounts = discounts
        self.member_service = member_service

        if len(self.cart_items) > 5:
            raise ValueError('max 5 items in a cart')

    def add(self, item: CartItem) -> int:
        if len(self.cart_items) == 5:
            raise ValueError(f'cannot add {item.product.name} because your cart has reached the purchase limit')

        index = next((i for i, it in enumerate(self.cart_items) if it.product.name == item.product.name), -1)
        if index >= 0:
            self.cart_items[index] = self.cart_items[index].add_quantity(item.quantity)
        else:
            self.cart_items.append(item)

        deduction = sum(discount.apply(self.cart_items) for discount in self.discounts)

        total_before_shipping_fee = sum(cart_item.subtotal for cart_item in self.cart_items) - int(deduction)
        if self.member_service.query_is_member_vip():
            shipping_fee = 0
        elif total_before_shipping_fee > 500:
            shipping_fee = 0
        else:
            shipping_fee = self.default_shipping_fee
        return total_before_shipping_fee + shipping_fee


class TestWhenAddingItemToCart(unittest.TestCase):
    def setUp(self):
        self.product_keyboard = Product(name='Keyboard', unit_price=800, max_purchase_quantity=1)
        self.product_mouse = Product(name='Computer Mouse', unit_price=500, max_purchase_quantity=1)
        self.product_pencil_sharpener = Product(name='Pencil Sharpener', unit_price=200, max_purchase_quantity=2)
        self.product_pencil = Product(name='Pencil', unit_price=20, max_purchase_quantity=10)
        self.product_eraser = Product(name='Eraser', unit_price=10, max_purchase_quantity=10)

    def given_cart_has(self, cart_items=None):
        if cart_items is None:
            cart_items = []
        self.cart = Cart(cart_items=cart_items, discounts=[], member_service=FakeMemberService())

    def test_total_should_be_the_sum_up_subtotals_of_all_items_plus_shipping_fee(self):
        # given
        self.given_cart_has([CartItem(5, self.product_eraser)])

        # when
        price = self.cart.add(CartItem(10, self.product_pencil))

        # then
        self.assertEqual(price, 310)

    def test_should_show_error_when_add_to_existing_items_that_is_more_tha_the_product_max_purchase_qty(self):
        # given
        self.given_cart_has([CartItem(10, self.product_eraser)])

        # when
        with pytest.raises(ValueError) as e:
            self.cart.add(CartItem(1, self.product_eraser))

        # then
        self.assertTrue('already reach the maximum purchase quantity of Eraser: 10' in str(e.value))

    def test_should_show_error_when_add_new_items_with_too_many_qty(self):
        # given
        self.given_cart_has()

        # when
        with pytest.raises(ValueError) as e:
            self.cart.add(CartItem(11, self.product_eraser))

        # then
        self.assertTrue('already reach the maximum purchase quantity of Eraser: 10' in str(e.value))

    def test_should_fail_given_cart_has_already_5_items(self):
        # given
        self.given_cart_has([
            CartItem(1, self.product_eraser),
            CartItem(1, self.product_pencil),
            CartItem(1, Product(name='Blue Pen', unit_price=30, max_purchase_quantity=10)),
            CartItem(1, Product(name='Notebook', unit_price=50, max_purchase_quantity=5)),
            CartItem(1, self.product_keyboard),
        ])

        # when
        with pytest.raises(ValueError) as e:
            self.cart.add(CartItem(1, Product(name='Pencil Sharpener', unit_price=200, max_purchase_quantity=2)))

        # then
        self.assertTrue('cannot add Pencil Sharpener because your cart has reached the purchase limit' in str(e.value))

    def test_should_free_shipping_when_cart_total_is_over_500(self):
        # given
        self.given_cart_has([CartItem(2, self.product_pencil_sharpener)])

        # when
        price = self.cart.add(CartItem(6, self.product_pencil))

        # then
        self.assertEqual(price, 520)

    def test_should_free_shipping_given_customer_is_VIP(self):
        # given
        cart = Cart(member_service=FakeMemberService(is_vip=True))

        # when
        price = cart.add(CartItem(1, self.product_pencil))

        # then
        self.assertEqual(price, 20)

    def test_quantity_discounts_should_be_applied_to_the_cart_items(self):
        # given
        cart = Cart(discounts=[
            QuantityDiscount(
                name='Pencil Day', product_name=self.product_pencil.name, quantity=10, discount_percentage=10),
        ])

        # when
        price = cart.add(CartItem(10, self.product_pencil))

        # then
        self.assertEqual(price, 180 + 60)

    def test_bundle_discounts_should_be_applied_to_the_cart_items(self):
        # given
        cart = Cart(cart_items=[
            CartItem(1, self.product_keyboard),
        ],
                    discounts=[
                        BundleDiscount(name='3C Day',
                                       product_a_name=self.product_keyboard.name,
                                       product_b_name=self.product_mouse.name,
                                       deduction_amount=300)
                    ])

        # when
        price = cart.add(CartItem(1, self.product_mouse))

        # then
        self.assertEqual(price, 1000)


class CartItemTest(unittest.TestCase):
    def test_quantity_should_not_surpass_product_maximum_purchase_qty(self):
        with pytest.raises(ValueError) as e:
            Cart([CartItem(11, Product('Pencil', 20, 10))])
        self.assertEqual('already reach the maximum purchase quantity of Pencil: 10', str(e.value))


class CartTest(unittest.TestCase):
    def test_maximum_cart_items_should_be_5(self):
        with pytest.raises(ValueError):
            Cart([
                CartItem(1, Product(name='Blue Pen1', unit_price=30, max_purchase_quantity=10)),
                CartItem(1, Product(name='Blue Pen2', unit_price=30, max_purchase_quantity=10)),
                CartItem(1, Product(name='Blue Pen', unit_price=30, max_purchase_quantity=10)),
                CartItem(1, Product(name='Notebook', unit_price=50, max_purchase_quantity=5)),
                CartItem(1, Product(name='Keyboard', unit_price=800, max_purchase_quantity=1)),
                CartItem(1, Product(name='Keyboard2', unit_price=800, max_purchase_quantity=1)),
            ])


class TestNewDiscount(unittest.TestCase):
    def test_should_show_error_when_adding_discount_with_invalid_discount_percentage(self):
        with pytest.raises(ValueError):
            Cart(discounts=[
                QuantityDiscount(name='Pencil Day', product_name='Pencil', quantity=10, discount_percentage=0)
            ])

    def test_should_fail_when_adding_discount_with_invalid_discount_amount(self):
        with pytest.raises(ValueError):
            Cart(discounts=[
                BundleDiscount(name='3C Day', product_a_name='Keyboard', product_b_name='Mouse', deduction_amount=0)
            ])

    def test_should_fail_when_two_identical_product(self):
        with pytest.raises(ValueError):
            Cart(discounts=[
                BundleDiscount(name='3C Day', product_a_name='Keyboard', product_b_name='Keyboard', deduction_amount=0)
            ])
