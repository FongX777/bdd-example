Feature:

  Scenario: Cart limit
    Given I'm in the shopping page
    And I put a pencil in the cart
    And I put an eraser in the cart
    And I put 3 pens in the cart
    And I put 2 houses in the cart
    And I put an airplane in the cart
    And I put a keyboard in the cart
    When I clicked the cart calculation button
    And the cart API result is back
    Then I can see an error in the http body: Cannot buy over 5 items'

  Scenario: All product price should be over o
    Given a baseball with price -100
    When I clicked the cart calculation button
    And the cart API result is back
    Then I can see the error : Invalid product'
