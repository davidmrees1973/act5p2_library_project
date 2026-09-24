# Exercise 4 - Unit Testing
# David Rees
#
# Simple example showing the Arrange, Act, Assert testing pattern.

def add_numbers(a, b):
    """Return the total of two numbers."""
    return a + b


def test_add_numbers():
    # ARRANGE - decide the input and expected result
    number1 = 2
    number2 = 3
    expected_result = 5

    # ACT - run the function being tested
    actual_result = add_numbers(number1, number2)

    # ASSERT - check that the result is what we expected
    assert actual_result == expected_result