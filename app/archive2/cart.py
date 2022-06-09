import abc
from typing import List


class Product:
    def __init__(self, name: str, price: float, max_purchase_qty: int):
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        self.name = name
        self.price = price
        self.max_purchase_qty = max_purchase_qty


class CartItem:
    # init product and qty
    def __init__(self, product: Product, qty: int):
        if qty > product.max_purchase_qty:
            raise ValueError(
                f'Cannot add more than {product.max_purchase_qty} of {product.name}'
            )
        self.product = product
        self.qty = qty

    @property
    def subtotal(self):
        return self.product.price * self.qty


class Discount(abc.ABC):
    @abc.abstractmethod
    def deduct(self, cart_items: List[CartItem]) -> float:
        pass


class BundleDiscount(Discount):
    def __init__(self, product_a_name: str, product_b_name: str,
                 deduction_amount: int):
        self.product_a_name = product_a_name
        self.product_b_name = product_b_name
        self.deduction_amount = deduction_amount

    def deduct(self, cart_items: List[CartItem]) -> float:
        matched_product_a = [
            item for item in cart_items
            if item.product.name == self.product_a_name
        ]
        matched_product_b = [
            item for item in cart_items
            if item.product.name == self.product_b_name
        ]

        if not matched_product_a or not matched_product_b:
            return 0
        deduction_times = min(matched_product_a[0].qty,
                              matched_product_b[0].qty)
        return self.deduction_amount * deduction_times


class QtyDiscount(Discount):
    def __init__(self, product_name: str, qty: int,
                 discount_percentage_off: int):
        self.product_name = product_name
        self.qty = qty
        self.discount_percentage_off = discount_percentage_off

    def deduct(self, cart_items: List[CartItem]) -> float:
        matched_product = [
            item for item in cart_items
            if item.product.name == self.product_name
        ]
        if not matched_product:
            return 0
        matched = matched_product[0]
        if matched.qty >= self.qty:
            times = int(matched.qty / self.qty)
            return (matched.product.price * self.qty *
                    self.discount_percentage_off / 100) * times
        return 0.0


class Cart:
    # init with discounts
    def __init__(self, discounts: List[Discount] = None):
        if discounts is None:
            discounts = []
        self.discounts = discounts

    def calculate(self, cart_items: List[CartItem]):
        if len(cart_items) > 5:
            raise ValueError('Cart cannot have more than 5 items')
        deduct_price = sum(
            discount.deduct(cart_items) for discount in self.discounts)
        return sum(cart_item.subtotal
                   for cart_item in cart_items) - deduct_price
