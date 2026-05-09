# tests/unit/test_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from typing import Union  # Import Union for type hinting multiple possible types
from app.operations import add, subtract, multiply, divide, modulus, power, root, absdiff # Import the calculator functions from the operations module

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]


# ---------------------------------------------
# Unit Tests for the 'add' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),           # Test adding two positive integers
        (-2, -3, -5),        # Test adding two negative integers
        (2.5, 3.5, 6.0),     # Test adding two positive floats
        (-2.5, 3.5, 1.0),    # Test adding a negative float and a positive float
        (0, 0, 0),            # Test adding zeros
    ],
    ids=[
        "add_two_positive_integers",
        "add_two_negative_integers",
        "add_two_positive_floats",
        "add_negative_and_positive_float",
        "add_zeros",
    ]
)
def test_add(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'add' function with various combinations of integers and floats.

    This parameterized test verifies that the 'add' function correctly adds two numbers,
    whether they are positive, negative, integers, or floats. By using parameterization,
    we can efficiently test multiple scenarios without redundant code.

    Parameters:
    - a (Number): The first number to add.
    - b (Number): The second number to add.
    - expected (Number): The expected result of the addition.

    Steps:
    1. Call the 'add' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_add(2, 3, 5)
    >>> test_add(-2, -3, -5)
    """
    # Call the 'add' function with the provided arguments
    result = add(a, b)
    
    # Assert that the result of add(a, b) matches the expected value
    assert result == expected, f"Expected add({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'subtract' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),           # Test subtracting a smaller positive integer from a larger one
        (-5, -3, -2),        # Test subtracting a negative integer from another negative integer
        (5.5, 2.5, 3.0),     # Test subtracting two positive floats
        (-5.5, -2.5, -3.0),  # Test subtracting two negative floats
        (0, 0, 0),            # Test subtracting zeros
    ],
    ids=[
        "subtract_two_positive_integers",
        "subtract_two_negative_integers",
        "subtract_two_positive_floats",
        "subtract_two_negative_floats",
        "subtract_zeros",
    ]
)
def test_subtract(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'subtract' function with various combinations of integers and floats.

    This parameterized test verifies that the 'subtract' function correctly subtracts the
    second number from the first, handling both positive and negative values, as well as
    integers and floats. Parameterization allows for comprehensive testing of multiple cases.

    Parameters:
    - a (Number): The number from which to subtract.
    - b (Number): The number to subtract.
    - expected (Number): The expected result of the subtraction.

    Steps:
    1. Call the 'subtract' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_subtract(5, 3, 2)
    >>> test_subtract(-5, -3, -2)
    """
    # Call the 'subtract' function with the provided arguments
    result = subtract(a, b)
    
    # Assert that the result of subtract(a, b) matches the expected value
    assert result == expected, f"Expected subtract({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'multiply' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),           # Test multiplying two positive integers
        (-2, 3, -6),         # Test multiplying a negative integer with a positive integer
        (2.5, 4.0, 10.0),    # Test multiplying two positive floats
        (-2.5, 4.0, -10.0),  # Test multiplying a negative float with a positive float
        (0, 5, 0),            # Test multiplying zero with a positive integer
    ],
    ids=[
        "multiply_two_positive_integers",
        "multiply_negative_and_positive_integer",
        "multiply_two_positive_floats",
        "multiply_negative_float_and_positive_float",
        "multiply_zero_and_positive_integer",
    ]
)
def test_multiply(a: Number, b: Number, expected: Number) -> None:
    """
    Test the 'multiply' function with various combinations of integers and floats.

    This parameterized test verifies that the 'multiply' function correctly multiplies two numbers,
    handling both positive and negative values, as well as integers and floats. Parameterization
    enables efficient testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The first number to multiply.
    - b (Number): The second number to multiply.
    - expected (Number): The expected result of the multiplication.

    Steps:
    1. Call the 'multiply' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_multiply(2, 3, 6)
    >>> test_multiply(-2, 3, -6)
    """
    # Call the 'multiply' function with the provided arguments
    result = multiply(a, b)
    
    # Assert that the result of multiply(a, b) matches the expected value
    assert result == expected, f"Expected multiply({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Unit Tests for the 'divide' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),           # Test dividing two positive integers
        (-6, 3, -2.0),         # Test dividing a negative integer by a positive integer
        (6.0, 3.0, 2.0),       # Test dividing two positive floats
        (-6.0, 3.0, -2.0),     # Test dividing a negative float by a positive float
        (0, 5, 0.0),            # Test dividing zero by a positive integer
    ],
    ids=[
        "divide_two_positive_integers",
        "divide_negative_integer_by_positive_integer",
        "divide_two_positive_floats",
        "divide_negative_float_by_positive_float",
        "divide_zero_by_positive_integer",
    ]
)
def test_divide(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'divide' function with various combinations of integers and floats.

    This parameterized test verifies that the 'divide' function correctly divides the first
    number by the second, handling both positive and negative values, as well as integers
    and floats. Parameterization allows for efficient and comprehensive testing across multiple cases.

    Parameters:
    - a (Number): The dividend.
    - b (Number): The divisor.
    - expected (float): The expected result of the division.

    Steps:
    1. Call the 'divide' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_divide(6, 3, 2.0)
    >>> test_divide(-6, 3, -2.0)
    """
    # Call the 'divide' function with the provided arguments
    result = divide(a, b)
    
    # Assert that the result of divide(a, b) matches the expected value
    assert result == expected, f"Expected divide({a}, {b}) to be {expected}, but got {result}"


# ---------------------------------------------
# Negative Test Case: Division by Zero
# ---------------------------------------------

def test_divide_by_zero() -> None:
    """
    Test the 'divide' function with division by zero.

    This negative test case verifies that attempting to divide by zero raises a ValueError
    with the appropriate error message. It ensures that the application correctly handles
    invalid operations and provides meaningful feedback to the user.

    Steps:
    1. Attempt to call the 'divide' function with arguments 6 and 0, which should raise a ValueError.
    2. Use pytest's 'raises' context manager to catch the expected exception.
    3. Assert that the error message contains "Cannot divide by zero!".

    Example:
    >>> test_divide_by_zero()
    """
    # Use pytest's context manager to check for a ValueError when dividing by zero
    with pytest.raises(ValueError) as excinfo:
        # Attempt to divide 6 by 0, which should raise a ValueError
        divide(6, 0)
    
    # Assert that the exception message contains the expected error message
    assert "Cannot divide by zero!" in str(excinfo.value), \
        f"Expected error message 'Cannot divide by zero!', but got '{excinfo.value}'"

### ---------------------------------------------
# Unit Tests for the 'modulus' Function
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 2, 1),           # Test modulus of two positive integers
        (5.5, 2, 1.5),       # Test modulus of a positive float by a positive integer
        (5, 2.5, 0.0),       # Test modulus of a positive integer by a positive float
        (-5, 2, 1),          # Test modulus of a negative integer by a positive integer
        (5, -2, -1),         # Test modulus of a positive integer by a negative integer
    ],
    ids=[
        "modulus_two_positive_integers",
        "modulus_positive_float_by_positive_integer",
        "modulus_positive_integer_by_positive_float",
        "modulus_negative_integer_by_positive_integer",
        "modulus_positive_integer_by_negative_integer",
    ]
)
def test_modulus(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'modulus' function with various combinations of integers and floats.

    This parameterized test verifies that the 'modulus' function correctly calculates the
    remainder of the division of the first number by the second, handling both positive
    and negative values, as well as integers and floats. Parameterization allows for efficient
    testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The dividend.
    - b (Number): The divisor.
    - expected (Number): The expected result of the modulus operation.

    Steps:
    1. Call the 'modulus' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_modulus(5, 2, 1)
    >>> test_modulus(5.5, 2, 1.5)
    """
    # Call the 'modulus' function with the provided arguments
    result = modulus(a, b)
    
    # Assert that the result of modulus(a, b) matches the expected value
    assert result == expected, f"Expected modulus({a}, {b}) to be {expected}, but got {result}"

def test_modulus_by_zero() -> None:
    """
    Test the 'modulus' function with modulus by zero.

    This negative test case verifies that attempting to perform modulus by zero raises a ValueError
    with the appropriate error message. It ensures that the application correctly handles
    invalid operations and provides meaningful feedback to the user.

    Steps:
    1. Attempt to call the 'modulus' function with arguments 5 and 0, which should raise a ValueError.
    2. Use pytest's 'raises' context manager to catch the expected exception.
    3. Assert that the error message contains "Cannot modulus by zero!".

    Example:
    >>> test_modulus_by_zero()
    """
    # Use pytest's context manager to check for a ValueError when performing modulus by zero
    with pytest.raises(ValueError) as excinfo:
        # Attempt to perform modulus of 5 by 0, which should raise a ValueError
        modulus(5, 0)
    
    # Assert that the exception message contains the expected error message
    assert "Cannot perform modulus by zero!" in str(excinfo.value), \
        f"Expected error message 'Cannot perform modulus by zero!', but got '{excinfo.value}'"
    
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 8),           # Test 2 raised to the power
        (5, 0, 1),           # Test any number raised to the power of 0
        (2.5, 3, 15.625),    # Test a positive float raised to a positive integer
        (2, -1, 0.5),        # Test a positive integer raised to a negative integer
        (-2, 3, -8),         # Test a negative integer raised to an odd positive integer
    ],
    ids=[
        "power_positive_integer",
        "power_zero_exponent",
        "power_positive_float_by_positive_integer",
        "power_positive_integer_by_negative_integer",
        "power_negative_integer_by_odd_positive_integer",
    ]
)
def test_power(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'power' function with various combinations of integers and floats.

    This parameterized test verifies that the 'power' function correctly calculates the
    result of raising the first number to the power of the second, handling both positive
    and negative values, as well as integers and floats. Parameterization allows for efficient
    testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The base number.
    - b (Number): The exponent.
    - expected (Number): The expected result of the power operation.

    Steps:
    1. Call the 'power' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_power(2, 3, 8)
    >>> test_power(5, 0, 1)
    """
    # Call the 'power' function with the provided arguments
    result = power(a, b)
    
    # Assert that the result of power(a, b) matches the expected value
    assert result == expected, f"Expected power({a}, {b}) to be {expected}, but got {result}"

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (27, 3, 3),          # Test the cube root of a perfect cube
        (16, 4, 2),          # Test the fourth root of a perfect fourth power
        (9, 2, 3),           # Test the square root of a perfect square
        (0, 3, 0),           # Test the root of zero
        (8, 3, 2),           # Test the cube root of a perfect cube
    ],
    ids=[
        "root_cube_of_perfect_cube",
        "root_fourth_of_perfect_fourth_power",
        "root_square_of_perfect_square",
        "root_of_zero",
        "root_cube_of_perfect_cube_2",  
    ]
)
def test_root(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'root' function with various combinations of integers and floats.

    This parameterized test verifies that the 'root' function correctly calculates the
    b-th root of a, handling both positive and negative values, as well as integers and floats.
    Parameterization allows for efficient testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The number to find the root of.
    - b (Number): The degree of the root.
    - expected (Number): The expected result of the root operation.

    Steps:
    1. Call the 'root' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_root(27, 3, 3)
    >>> test_root(16, 4, 2)
    """
    # Call the 'root' function with the provided arguments
    result = root(a, b)
    
    # Assert that the result of root(a, b) matches the expected value
    assert result == expected, f"Expected root({a}, {b}) to be {expected}, but got {result}"

def test_root_by_zero() -> None:
    """
    Test the 'root' function with root by zero.

    This negative test case verifies that attempting to perform root with zero as the degree raises a ValueError
    with the appropriate error message. It ensures that the application correctly handles
    invalid operations and provides meaningful feedback to the user.

    Steps:
    1. Attempt to call the 'root' function with arguments 16 and 0, which should raise a ValueError.
    2. Use pytest's 'raises' context manager to catch the expected exception.
    3. Assert that the error message contains "Cannot take root with zero as degree!".

    Example:
    >>> test_root_by_zero()
    """
    # Use pytest's context manager to check for a ValueError when performing root by zero
    with pytest.raises(ValueError) as excinfo:
        # Attempt to perform root of 16 by 0, which should raise a ValueError
        root(16, 0)
    
    # Assert that the exception message contains the expected error message
    assert "Cannot find root of zero!" in str(excinfo.value), \
        f"Expected error message 'Cannot find root of zero!', but got '{excinfo.value}'"
    

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),           # Test absolute difference of two positive integers
        (-5, 3, 8),          # Test absolute difference of a negative integer and a positive integer
        (5.5, 2.5, 3.0),    # Test absolute difference of two positive floats
        (-5.5, -2.5, 3.0),   # Test absolute difference of two negative floats
        (0, 5, 5),            # Test absolute difference of zero and a positive integer
    ],
    ids=[
        "absdiff_two_positive_integers",
        "absdiff_negative_and_positive_integer",
        "absdiff_two_positive_floats",
        "absdiff_two_negative_floats",
        "absdiff_zero_and_positive_integer",
    ]
)
def test_absdiff(a: Number, b: Number, expected: float) -> None:
    """
    Test the 'absdiff' function with various combinations of integers and floats.

    This parameterized test verifies that the 'absdiff' function correctly calculates the
    absolute difference between two numbers, handling both positive and negative values, as well as integers and floats.
    Parameterization allows for efficient testing of multiple scenarios in a concise manner.

    Parameters:
    - a (Number): The first number.
    - b (Number): The second number.
    - expected (Number): The expected result of the absolute difference operation.

    Steps:
    1. Call the 'absdiff' function with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Example:
    >>> test_absdiff(5, 3, 2)
    >>> test_absdiff(-5, 3, 8)
    """
    # Call the 'absdiff' function with the provided arguments
    result = absdiff(a, b)
    
    # Assert that the result of absdiff(a, b) matches the expected value
    assert result == expected, f"Expected absdiff({a}, {b}) to be {expected}, but got {result}"