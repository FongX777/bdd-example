# BDD Example

## Business Rules

### User Story:

As a customer,
I want to see the price in my shopping cart,
So that I can decide if I want to buy it.

### API Interface

- Input
    - Product id, Quantity
- Output
    - Product id, name, Quantity, Subtotal
    - Discount deduction subtotal
    - Total price

### Example Data

Products:

| Name             | Unit Price | Max Purchase |
|------------------|------------|--------------|
| Eraser           | 10         | 10           |
| Pencil           | 20         | 10           |
| Blue Pen         | 30         | 10           |
| Ruler            | 35         | 10           |
| Notebook         | 50         | 5            |
| Pencil Sharpener | 200        | 2            |
| Computer Mouse   | 500        | 1            |
| Keyboard         | 800        | 1            |

### Acceptance Criteria:

There are 3 releases:

1. Release 1:
    1. no discounts
    2. the cart only need to return the total price
2. Release 2:
    1. discounts
    2. the cart needs to return subtotal of all items including discounts
3. Release 3:
    1. Customer can know how discounts are applied

---

1. Cart
    1. a cart item can be either a product or a matched discount
    2. a cart item has a quantity and a price, and the subtotal is the quantity times the price
    3. It's not allowed to have two cart items that are the same product (you should add the quantity instead)
    4. a cart cannot have over 5 kinds of products
    5. [hide] the total of the cart cannot be negative
    6. [hide] the quantity of a product in the cart should not exceed the maximum purchase quantity of the product
    7. [hide] the total of the cart is the sum of the subtotals of all cart items
2. Product
    1. a product has a name, a unit price, and max purchase quantity
    2. unit price cannot be 0 or negative
    3. a product can be matched with a discount
3. Discount
    1. a discount has a name, a discount rate, and criteria
    2. one discount can only be applied multiple times if criteria is satisfied
        1. [hide] discounts are not exclusive to each other
    3. currently, there are two kinds of discounts:
        1. Single product quantity discount
        2. A plus B discount
4. Single product quantity discount with percent discount rate
    1. a discount has a discount name, a discount rate, and an associated product
    2. Buy x quantity get y percent off
    3. Discount rate can only be 5, 10, 15 percent
    4. The deduction amount should be rounded off
    5. [hide] the criteria quantity should be above 1, but must not exceed the max purchase quantity of the
       associated product
5. A plus B bundle discount with fixed price discount rate
    1. a discount has a discount name, a fixed discount deduction amount, and two associated products
    2. The two associated products cannot be the same product
    3. One A product and one B product can be combined to get a discount of x deduction amount

