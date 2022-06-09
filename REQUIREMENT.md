# Requirement

## 功能：加商品至購物車

客人可以把商品以及欲購買數量加入購物，並得到目前的購物車總金額。
一次只能加入一項（商品以及指定數量）

1. 購物車金總價是每一細項的總和，一個細項是商品單價乘上數量，加上物流費 60 元
2. 加入的商品數量不可以超商品可購買上限，如果超過，要警示客人，並標示出該商品已經到達購買上限
3. 購物車最多只能有 5 種商品，如果超過，要警示客人不能這樣做，並標示出是哪一項商品不能加入。
4. 超過 500 元則免運費
5. (隱藏) 若是加入相同商品，則會加回原先的細項上，同時不能超過可購買上限
5. (隱藏) 若是加入相同商品，則會加回原先的細項上

一個商品有以下規則：

1. 名稱，不會有重複名稱
2. 單價，以 NTD 計算
3. 最大購買數量

### 目前商品列表：

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

## 進階功能：折扣計算

當商品加入購物車，如果當下商家有設定折扣，則會套用折扣計算總價。
目前可以設定的折扣有兩種：數量折扣與 A+B 折扣

1. 數量折扣：購買某商至指定數量時，可以享用折扣趴數
    1. 單一的指定商品，買到數量 X 時，可以享用折扣趴數 Y
    2. 折扣趴數只能是 5%, 10%, 15%
2. A+B 折扣：購買指定 A 商品與 B 商品時，可以享用金額減免
    1. 單一的指定商品，買到數量 X 時，可以享用金額減免 Y
    2. 金額減免是固定數字
    3. A 跟 B 不能是同一個商品

當購物車內的商品符合任一折扣時，就會進行打折，並回傳打折後的總金額。


---

4. Cart
    1. a cart item can be either a product or a matched discount
    2. a cart item has a quantity and a price, and the subtotal is the quantity times the price
    3. It's not allowed to have two cart items that are the same product (you should add the quantity instead)
    4. a cart cannot have over 5 kinds of products
    5. [hide] the total of the cart cannot be negative
    6. [hide] the quantity of a product in the cart should not exceed the maximum purchase quantity of the product
    7. [hide] the total of the cart is the sum of the subtotals of all cart items
5. Product
    1. a product has a name, a unit price, and max purchase quantity
    2. unit price cannot be 0 or negative
6. Discount
    1. a discount has a name, a discount rate, and criteria
    2. one discount can only be applied multiple times if criteria is satisfied
        1. [hide] discounts are not exclusive to each other
    3. currently, there are two kinds of discounts:
        1. Single product quantity discount
        2. A plus B discount
7. Single product quantity discount with percent discount rate
    1. a discount has a discount name, a discount rate, and an associated product
    2. Buy x quantity get y percent off
    3. Discount rate can only be 5, 10, 15 percent
    4. The deduction amount should be rounded off
    5. [hide] the criteria quantity should be above 1, but must not exceed the max purchase quantity of the
       associated product
8. A plus B bundle discount with fixed price discount rate
    1. a discount has a discount name, a fixed discount deduction amount, and two associated products
    2. The two associated products cannot be the same product
    3. One A product and one B product can be combined to get a discount of x deduction amount
