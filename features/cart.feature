Feature: Add to cart

  As a customer,
  I want to add products to my cart and see the current total
  So that I can proceed my purchase


  Background:
    Given a sample price list:
      | Name               | Unit Price   | Max Purchase   |
      | ------------------ | ------------ | -------------- |
      | Eraser             | 10           | 10             |
      | Pencil             | 20           | 10             |
      | Blue Pen           | 30           | 10             |
      | Ruler              | 35           | 10             |
      | Notebook           | 50           | 5              |
      | Pencil Sharpener   | 200          | 2              |
      | Computer Mouse     | 500          | 1              |
      | Keyboard           | 800          | 1              |

  Scenario: Cart total should be the sum of each item subtotal plus shipping fee 60
    Given the cart has 5 erasers
    When the customer adds 10 pencils to the cart
    Then the total should be 310

  Scenario: Cannot buy over the the max purchase quantity when adding quantity to existing items
    Given the cart has 10 erasers
    When the customer adds 1 eraser
    Then the system should show error: "You already reach the maximum purchase quantity of eraser: 10"

  Scenario: Cannot buy over the the max purchase quantity when adding new item
    Given the cart is empty
    When the customer adds 11 eraser
    Then the system should show error: "You already reach the maximum purchase quantity of eraser: 10"

  Scenario: Maximum 5 items in a cart
    Given the cart has 1 eraser, 1 pencil, 1 blue pen, 1 notebook, and 1 keyboard
    When the customer adds 1 pencil sharpener
    Then the system should show error: "You cannot add pencil sharpener because your cart has reached the purchase limit"

  Scenario Outline: Free shipping fee when cart total is over 500
    Given the cart has 2 Pencil Sharpeners
    When the customer adds <pencil_count> pencils
    Then the shipping fee should be <is_included>
    And the total should be <total>

    Examples:
      | pencil_count | is_included  | total |
      | 5            | not included | 560   |
      | 6            | included     | 520   |

  Scenario: Quantity discounts should be considered in cart total
    Given today has a discount "Pencil Day" that 10 pencils have 10% off
    When the customer adds 10 pencil
    Then the discount deduction should be 20
    Then the total should be 240 (shipping fee included)

  Scenario: Deduction number from quantity discount should be round off
    Given today has a discount "Ruler Day" that 3 rulers have 5% off
    When the customer adds 3 rulers
    Then the discount deduction should be 6
    And the total should be 165 (shipping fee included)

  Scenario: A+B Bundle discounts should be considered in cart total
    Given today has a discount "3C Day" that the bundle of keyboard and computer mouse receives 300 NTD deduction
    And the cart has 1 keyboard
    When the customer adds 1 computer mouse
    Then the total should be 1000 (free shipping)

  Scenario: VIP can be free of shipping fee
    Given Sean is a VIP member
    When the customer adds 1 computer mouse
    Then the shipping fee is 0
    And the total should be 500
