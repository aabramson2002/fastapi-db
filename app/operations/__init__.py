# app/operations.py

"""
Module: operations.py

This module contains basic arithmetic functions that perform addition, subtraction,
multiplication, and division of two numbers. These functions are foundational for
building more complex applications, such as calculators or financial tools.

Functions:
- add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the sum of a and b.
- subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the difference when b is subtracted from a.
- multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the product of a and b.
- divide(a: Union[int, float], b: Union[int, float]) -> float: Returns the quotient when a is divided by b. Raises ValueError if b is zero.
- modulus(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the remainder of a divided by b. Raises ValueError if b is zero.
- power(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns a raised to the power of b.
- root(a: Union[int, float], b: Union[int, float]) -> float: Returns the b-th root of a. Raises ValueError if b is zero.
- absdiff(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the absolute difference between a and b.

Usage:
These functions can be imported and used in other modules or integrated into APIs
to perform arithmetic operations based on user input.
"""

from typing import Union  # Import Union for type hinting multiple possible types

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """
    Add two numbers and return the result.

    Parameters:
    - a (int or float): The first number to add.
    - b (int or float): The second number to add.

    Returns:
    - int or float: The sum of a and b.

    Example:
    >>> add(2, 3)
    5
    >>> add(2.5, 3)
    5.5
    """
    # Perform addition of a and b
    result = a + b
    return result

def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first and return the result.

    Parameters:
    - a (int or float): The number from which to subtract.
    - b (int or float): The number to subtract.

    Returns:
    - int or float: The difference between a and b.

    Example:
    >>> subtract(5, 3)
    2
    >>> subtract(5.5, 2)
    3.5
    """
    # Perform subtraction of b from a
    result = a - b
    return result

def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers and return the product.

    Parameters:
    - a (int or float): The first number to multiply.
    - b (int or float): The second number to multiply.

    Returns:
    - int or float: The product of a and b.

    Example:
    >>> multiply(2, 3)
    6
    >>> multiply(2.5, 4)
    10.0
    """
    # Perform multiplication of a and b
    result = a * b
    return result

def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second and return the quotient.

    Parameters:
    - a (int or float): The dividend.
    - b (int or float): The divisor.

    Returns:
    - float: The quotient of a divided by b.

    Raises:
    - ValueError: If b is zero, as division by zero is undefined.

    Example:
    >>> divide(6, 3)
    2.0
    >>> divide(5.5, 2)
    2.75
    >>> divide(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero!
    """
    # Check if the divisor is zero to prevent division by zero
    if b == 0:
        # Raise a ValueError with a descriptive message
        raise ValueError("Cannot divide by zero!")
    
    # Perform division of a by b and return the result as a float
    result = a / b
    return result

def modulus(a: Number, b: Number) -> Number:
    """
    Return the remainder of the division of a by b.

    Parameters:
    - a (int or float): The dividend.
    - b (int or float): The divisor.

    Returns:
    - int or float: The remainder of a divided by b.

    Raises:
    - ValueError: If b is zero, as modulus by zero is undefined.

    Example:
    >>> modulus(5, 2)
    1
    >>> modulus(5.5, 2)
    1.5
    >>> modulus(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot perform modulus by zero!
    """
    # Check if the divisor is zero to prevent modulus by zero
    if b == 0:
        # Raise a ValueError with a descriptive message
        raise ValueError("Cannot perform modulus by zero!")
    
    # Perform modulus of a by b and return the result
    result = a % b
    return result

def power(a: Number, b: Number) -> Number:
    """
    Return a raised to the power of b.

    Parameters:
    - a (int or float): The base number.
    - b (int or float): The exponent.

    Returns:
    - int or float: The result of a raised to the power of b.

    Example:
    >>> power(2, 3)
    8
    >>> power(5, 0)
    1
    >>> power(2, -1)
    0.5
    """
    # Perform exponentiation of a by b and return the result
    result = a ** b
    return result

def root(a: Number, b: Number) -> float:
    """
    Return the b-th root of a.

    Parameters:
    - a (int or float): The number to find the root of.
    - b (int or float): The degree of the root.

    Returns:
    - float: The b-th root of a.

    Raises:
    - ValueError: If b is zero, as root of zero is undefined.

    Example:
    >>> root(27, 3)
    3.0
    >>> root(16, 4)
    2.0
    >>> root(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot find root of zero!
    """
    # Check if the degree of the root is zero to prevent undefined behavior
    if b == 0:
        # Raise a ValueError with a descriptive message
        raise ValueError("Cannot find root of zero!")
    if a < 0 and b % 2 == 0:
        # Raise a ValueError if trying to take an even root of a negative number
        raise ValueError("Cannot take even root of a negative number!")
    
    # Perform root calculation using exponentiation and return the result as a float
    result = a ** (1 / b)
    return result

def absdiff(a: Number, b: Number) -> Number:
    """
    Return the absolute difference between two numbers.

    Parameters:
    - a (int or float): The first number.
    - b (int or float): The second number.

    Returns:
    - int or float: The absolute difference between a and b.

    Example:
    >>> absdiff(5, 3)
    2
    >>> absdiff(3, 5)
    2
    >>> absdiff(5.5, 2.5)
    3.0
    """
    # Calculate the absolute difference using the built-in abs function
    result = abs(a - b)
    return result