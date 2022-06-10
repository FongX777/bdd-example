# BDD Example

This is a workshop material for writing BDD style tests to design your code.

- [Requirement](./REQUIREMENT.md) ([ZH](./REQUIREMENT-zh.md))

## Three steps

We will go through the following steps:

1. Discovery: Discover the requirements with concrete example through [example mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/).
2. Formulation: Formulate the concrete examples into a business-readable specification document through gherkin.
3. Automation: Design and write the test cases according to the business-readable specification document.

### Step 1 - Discovery (Example Mapping)

We will use example mapping workshop to discover the requirements and uncover ambiguities with team members.

After this step, we will get a bunch of concrete examples that illustrate how our system will be actually used by the users.

- Input: a user story or a feature, and some details about the user story
- Output: a bunch of concrete examples that explain the rules of the user story, which can be regarded as the acceptance criteria of the user story.
- Tips:
    - Focus on exploration and discover what you don't know before the workshop
    - A good example usually use real numbers and happens in real situations, and consists of the context and the expected result, which can be validated.
    - Don't be strict on the format of the examples, we'll refine the wording and the format later on in Step 2. You can use a sentence or even a data table to describe examples
    - Examples should be focused and highly related to the rule it belongs to, don't try to write an example to explain multiple rules

The sample output is in [TODO: add a pic]

### Step 2 - Formulation (Gherkin)

Formulate the concrete examples into a business-readable specification document through gherkin. to make sure all team members are on the same page.

- Input: a bunch of concrete examples
- Output: a gherkin document (a `xxx.feature` file)
- Tips:
    - Be selective and don't forget your goal is to write a user-friendly and business-rich document, not an E2E script.
    - **A rule is usually mapped to a `Scenario`**, and you can pick some key examples that reveals the intention the most to flesh out your `Given`, `When`, and `Then`.
    - Remove redundant details in the examples and make the gherkin document more concise and readable.
    - In the real world, you can have a tester and a dev to co-write the document, and let product owner to review the final work.

The sample output is in [cart.feature](./features/cart.feature).

### Step 3 - Automation

The final step is automation, which we design and write the test cases according to the business-readable specification document.

In this tutorial, we don't use some popular frameworks or tools like Cucumber or Jebehave. Instead, we prefer to write BDD-liked tests based on the built-in testing framework.

First, you need to decide the name of your test class, instead of jumping into your SUT class name, we suggest you to use the name of your feature or the action you want to test. For example:

```python
# Bad
class TestCart:
    pass


# Better
class TestAddItemsToCart:
    pass
```

So we have a test class `TestAddItemsToCart`, and before we write the first test method, we have to come up with a good name for the test method. Here are 3 principles:

1. The test method name should be a readable sentence
2. Strongly suggest you to use "should" keyword at first, you can change it later on ([opposing opinion](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/))
3. You can adhere to this template, in which `given` and `when` are actually optional

Here's a template:

```
# python
def test_xxx_should_yyy_when_zzz_given_aaa()

# Java
@Test
public void should_xxx_when_yyy_when_given_zzz()

# JS/TS
it('should xxx when yyy when given zzz', () => {})
```

The sample code is in [test_cart.py](./app/test_cart.py).
