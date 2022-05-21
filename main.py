import abc
import copy
import dataclasses
from typing import List


@dataclasses.dataclass
class Product:
    id: int
    name: str
    unit_price: int
    max_purchase_amount: int


apple = Product(1, 'apple', 30, 3)
pencil = Product(2, 'pencil', 30, 2)
keyboard = Product(3, 'keyboard', 600, 1)
notebook = Product(4, 'notebook', 30, 4)


@dataclasses.dataclass
class CartItem:
    product: Product
    amount: int
    discount_off: int = 0

    @property
    def price(self):
        # rule: round off anyway
        return int(self.product.unit_price * self.amount *
                   (1 - self.discount_off * 0.01))

    def apply_discount_off(self, new_discount_off: int):
        return CartItem(product=self.product,
                        amount=self.amount,
                        discount_off=new_discount_off)


class Cart:
    # rule: 1 item for 1 kind of product
    def __init__(self, items: List[CartItem], allowed_discounts: List):
        self.items = items
        self.allowed_discounts = allowed_discounts

    def add_item(self, item):
        self.items.append(item)

    def calculate_price(self) -> int:
        calculated_items = copy.deepcopy(self.items)
        for discount in self.allowed_discounts:
            calculated_items = discount.apply(calculated_items)

        return sum(item.price for item in calculated_items)


class Discount(abc.ABC):
    @abc.abstractmethod
    def apply(self, cart_items: List[CartItem]):
        pass


class SinglePieceDiscount:
    def __init__(self,
                 product_id: int,
                 criteria_amount: int,
                 discount_off: int,
                 is_exclusive=False):
        self.discount_off = discount_off
        self.criteria_amount = criteria_amount
        self.is_exclusive = is_exclusive
        self.product_id = product_id

    def apply(self, cart_items: List[CartItem]):
        for i, item in enumerate(cart_items):
            if item.product.id == self.product_id:
                cart_items[i] = cart_items[i].apply_discount_off(
                    self.discount_off)
                break

        return cart_items


class ABDiscount:
    def __init__(self,
                 product_a_id: int,
                 product_b_id: int,
                 discount_off: int,
                 is_exclusive=False):
        self.discount_off = discount_off
        self.product_a_id = product_a_id  # product a cannot be equal to product b
        self.product_b_id = product_b_id
        self.is_exclusive = is_exclusive

    def apply(self, cart_items: List[CartItem]):
        matched = [None, None]

        for i, item in enumerate(cart_items):
            if item.product.id == self.product_a_id:
                matched[0] = i
            if item.product.id == self.product_b_id:
                matched[1] = i

        if matched[0] is not None and matched[1] is not None:
            cart_items[matched[0]].apply_discount_off(self.discount_off)
            cart_items[matched[1]].apply_discount_off(self.discount_off)

        return cart_items


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    discounts = [
        SinglePieceDiscount(product_id=apple.id,
                            criteria_amount=2,
                            discount_off=15,
                            is_exclusive=True),
        SinglePieceDiscount(product_id=notebook.id,
                            criteria_amount=3,
                            discount_off=15,
                            is_exclusive=True),
        ABDiscount(product_a_id=keyboard.id,
                   product_b_id=pencil.id,
                   discount_off=10,
                   is_exclusive=True),
        ABDiscount(product_a_id=apple.id,
                   product_b_id=pencil.id,
                   discount_off=5,
                   is_exclusive=True)
    ]

    interested_items = [
        CartItem(product=apple, amount=2),
        # CartItem(product=notebook, amount=3)
    ]

    cart = Cart(interested_items, allowed_discounts=discounts)

    print(cart.calculate_price())

    # rule: discount_of: 5%, 10%, 15%, 25%
    # rule: SinglePieceDiscount: criteria_amount should > 1
    # rule: SinglePieceDiscount: criteria_amount cannot be bigger than max purchase amount of the product

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
