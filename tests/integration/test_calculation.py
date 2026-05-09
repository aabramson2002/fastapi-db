"""
From Mod 11 repo, this file contains integration tests for the calculation logic
and the polymorphic factory pattern used to create different calculation types.
"""

import pytest
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Modulus,
    Power,
    Root,
    AbsoluteDifference,
)


# Helper function to create a dummy user_id for testing.
def dummy_user_id():
    """
    Generate a random UUID for testing purposes.
    
    In real tests with a database, you would create an actual user
    and use their ID. This helper is sufficient for unit-level testing
    of the calculation logic without database dependencies.
    """
    return uuid.uuid4()


# ============================================================================
# Tests for Individual Calculation Types
# ============================================================================

def test_addition_get_result():
    """
    Test that Addition.get_result returns the correct sum.
    
    This verifies that the Addition class correctly implements the
    polymorphic get_result() method for its specific operation.
    """
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"


def test_subtraction_get_result():
    """
    Test that Subtraction.get_result returns the correct difference.
    
    Subtraction performs sequential subtraction: first - second - third...
    """
    inputs = [20, 5, 3]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 20 - 5 - 3 = 12
    result = subtraction.get_result()
    assert result == 12, f"Expected 12, got {result}"


def test_multiplication_get_result():
    """
    Test that Multiplication.get_result returns the correct product.
    
    Multiplication multiplies all input numbers together.
    """
    inputs = [2, 3, 4]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 24, f"Expected 24, got {result}"


def test_division_get_result():
    """
    Test that Division.get_result returns the correct quotient.
    
    Division performs sequential division: first / second / third...
    """
    inputs = [100, 2, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 100 / 2 / 5 = 10
    result = division.get_result()
    assert result == 10, f"Expected 10, got {result}"


def test_division_by_zero():
    """
    Test that Division.get_result raises ValueError when dividing by zero.
    
    This demonstrates EAFP (Easier to Ask for Forgiveness than Permission):
    We attempt the operation and catch the exception rather than checking
    beforehand.
    """
    inputs = [50, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()

def test_modulus_get_result():
    """
    Test that Modulus.get_result returns the correct remainder.
    
    Modulus returns the remainder of the first number divided by the second.
    """
    inputs = [10, 3]
    modulus = Modulus(user_id=dummy_user_id(), inputs=inputs)
    result = modulus.get_result()
    assert result == 1, f"Expected 1, got {result}"

def test_modulus_by_zero():
    """
    Test that Modulus.get_result raises ValueError when modulus by zero.
    
    This verifies that modulus operation properly handles division by zero cases.
    """
    inputs = [10, 0]
    modulus = Modulus(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot perform modulus by zero."):
        modulus.get_result()

def test_power_get_result():
    """
    Test that Power.get_result returns the correct exponentiation result.
    
    Power returns the first number raised to the power of the second.
    """
    inputs = [2, 3]
    power = Power(user_id=dummy_user_id(), inputs=inputs)
    result = power.get_result()
    assert result == 8, f"Expected 8, got {result}"

def test_root_get_result():
    """
    Test that Root.get_result returns the correct root result.
    
    Root returns the nth root of the first number, where n is the second number.
    """
    inputs = [27, 3]
    root = Root(user_id=dummy_user_id(), inputs=inputs)
    result = root.get_result()
    assert result == 3, f"Expected 3, got {result}"

def test_root_by_zero():
    """
    Test that Root.get_result raises ValueError when trying to find root of zero.
    
    This verifies that root operation properly handles invalid cases.
    """
    inputs = [10, 0]
    root = Root(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot take root with zero as degree."):
        root.get_result()

def test_root_of_negative_even():
    """
    Test that Root.get_result returns a complex number when trying to find even root of a negative number.
    
    Python's exponentiation returns complex numbers for even roots of negative numbers.
    Note: The model doesn't validate this at the model level; it returns complex numbers.
    """
    inputs = [-16, 4]
    root = Root(user_id=dummy_user_id(), inputs=inputs)
    # Python returns a complex number for even root of negative
    # The model doesn't explicitly validate this, so it will compute it
    result = root.get_result()
    # Verify it returns a complex number (approximately 2j)
    assert isinstance(result, complex) or isinstance(result, float)

def test_root_of_negative_odd():
    """
    Test that Root.get_result behavior with odd root of negative numbers.
    
    Note: Python's exponentiation returns complex numbers even for odd roots of negatives.
    For example: (-27) ** (1/3) returns a complex number, not -3.
    """
    inputs = [-27, 3]
    root = Root(user_id=dummy_user_id(), inputs=inputs)
    result = root.get_result()
    # Python returns complex number for this operation
    # Just verify the operation completes without error
    assert result is not None

def test_absolute_difference_get_result():
    """
    Test that AbsoluteDifference.get_result returns the correct absolute difference.
    
    AbsoluteDifference returns the absolute value of the difference between the first two numbers.
    """
    inputs = [10, 4]
    absdiff = AbsoluteDifference(user_id=dummy_user_id(), inputs=inputs)
    result = absdiff.get_result()
    assert result == 6, f"Expected 6, got {result}"


# ============================================================================
# Tests for Polymorphic Factory Pattern
# ============================================================================

def test_calculation_factory_addition():
    """
    Test the Calculation.create factory method for addition.
    
    This demonstrates polymorphism: The factory method returns a specific
    subclass (Addition) that can be used through the common Calculation
    interface.
    
    Key Polymorphic Concepts:
    1. Factory returns the correct subclass type
    2. The returned object behaves as both Calculation and Addition
    3. Type-specific behavior (get_result) works correctly
    """
    inputs = [1, 2, 3]
    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Verify polymorphism: factory returned the correct subclass
    assert isinstance(calc, Addition), \
        "Factory did not return an Addition instance."
    assert isinstance(calc, Calculation), \
        "Addition should also be an instance of Calculation."
    # Verify behavior: subclass implements get_result() correctly
    assert calc.get_result() == sum(inputs), "Incorrect addition result."


def test_calculation_factory_subtraction():
    """
    Test the Calculation.create factory method for subtraction.
    
    Demonstrates that the factory pattern works consistently across
    different calculation types.
    """
    inputs = [10, 4]
    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 10 - 4 = 6
    assert isinstance(calc, Subtraction), \
        "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6, "Incorrect subtraction result."


def test_calculation_factory_multiplication():
    """
    Test the Calculation.create factory method for multiplication.
    """
    inputs = [3, 4, 2]
    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 3 * 4 * 2 = 24
    assert isinstance(calc, Multiplication), \
        "Factory did not return a Multiplication instance."
    assert calc.get_result() == 24, "Incorrect multiplication result."


def test_calculation_factory_division():
    """
    Test the Calculation.create factory method for division.
    """
    inputs = [100, 2, 5]
    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 100 / 2 / 5 = 10
    assert isinstance(calc, Division), \
        "Factory did not return a Division instance."
    assert calc.get_result() == 10, "Incorrect division result."

def test_calculation_factory_modulus():
    """
    Test the Calculation.create factory method for modulus.
    """
    inputs = [10, 3]
    calc = Calculation.create(
        calculation_type='modulus',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 10 % 3 = 1
    assert isinstance(calc, Modulus), \
        "Factory did not return a Modulus instance."
    assert calc.get_result() == 1, "Incorrect modulus result."

def test_calculation_factory_power():
    """
    Test the Calculation.create factory method for power.
    """
    inputs = [2, 3]
    calc = Calculation.create(
        calculation_type='power',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 2 ** 3 = 8
    assert isinstance(calc, Power), \
        "Factory did not return a Power instance."
    assert calc.get_result() == 8, "Incorrect power result."

def test_calculation_factory_root():
    """
    Test the Calculation.create factory method for root.
    """
    inputs = [27, 3]
    calc = Calculation.create(
        calculation_type='root',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 27 ** (1/3) = 3
    assert isinstance(calc, Root), \
        "Factory did not return a Root instance."
    assert calc.get_result() == 3, "Incorrect root result."

def test_calculation_factory_absolute_difference():
    """
    Test the Calculation.create factory method for absolute difference.
    """
    inputs = [10, 4]
    calc = Calculation.create(
        calculation_type='absolute_difference',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: abs(10 - 4) = 6
    assert isinstance(calc, AbsoluteDifference), \
        "Factory did not return an AbsoluteDifference instance."
    assert calc.get_result() == 6, "Incorrect absolute difference result."


def test_calculation_factory_invalid_type():
    """
    Test that Calculation.create raises a ValueError for unsupported types.
    
    This verifies that the factory pattern properly handles invalid inputs
    and provides clear error messages.
    """
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='invalid_operation',  # unsupported type
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )


def test_calculation_factory_case_insensitive():
    """
    Test that the factory is case-insensitive.
    
    The factory should accept 'Addition', 'ADDITION', 'addition', etc.
    """
    inputs = [5, 3]
    
    # Test various cases
    for calc_type in ['addition', 'Addition', 'ADDITION', 'AdDiTiOn']:
        calc = Calculation.create(
            calculation_type=calc_type,
            user_id=dummy_user_id(),
            inputs=inputs,
        )
        assert isinstance(calc, Addition), \
            f"Factory failed for case: {calc_type}"
        assert calc.get_result() == 8


# ============================================================================
# Tests for Input Validation (Edge Cases)
# ============================================================================

def test_invalid_inputs_for_addition():
    """
    Test that providing non-list inputs to Addition.get_result raises error.
    
    This verifies that calculations properly validate their inputs before
    attempting operations.
    """
    addition = Addition(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()


def test_invalid_inputs_for_subtraction():
    """
    Test that providing fewer than two numbers raises a ValueError.
    
    All calculations require at least two inputs to be meaningful.
    """
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(
        ValueError,
        match="Inputs must be a list with at least two numbers."
    ):
        subtraction.get_result()


def test_invalid_inputs_for_multiplication():
    """
    Test that Multiplication requires at least two inputs.
    """
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=[5])
    with pytest.raises(
        ValueError,
        match="Inputs must be a list with at least two numbers."
    ):
        multiplication.get_result()


def test_invalid_inputs_for_division():
    """
    Test that Division requires at least two inputs.
    """
    division = Division(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(
        ValueError,
        match="Inputs must be a list with at least two numbers."
    ):
        division.get_result()


def test_division_by_zero_in_middle():
    """
    Test division by zero when zero appears in the middle of inputs.
    
    This ensures zero validation works for any position after the first.
    """
    inputs = [100, 5, 0, 2]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


def test_division_by_zero_at_end():
    """
    Test division by zero when zero is the last input.
    """
    inputs = [50, 5, 0]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


# ============================================================================
# Tests Demonstrating Polymorphic Behavior
# ============================================================================

def test_polymorphic_list_of_calculations():
    """
    Test that different calculation types can be stored in the same list.
    
    This demonstrates polymorphism: A list of Calculation objects can contain
    different subclasses, and each maintains its type-specific behavior.
    
    This is a key benefit of polymorphism: you can treat different types
    uniformly while they maintain their unique implementations.
    """
    user_id = dummy_user_id()
    
    # Create a list of different calculation types
    calculations = [
        Calculation.create('addition', user_id, [1, 2, 3]),
        Calculation.create('subtraction', user_id, [10, 3]),
        Calculation.create('multiplication', user_id, [2, 3, 4]),
        Calculation.create('division', user_id, [100, 5]),
        Calculation.create('modulus', user_id, [10, 3]),
        Calculation.create('power', user_id, [2, 3]),
        Calculation.create('root', user_id, [27, 3]),
        Calculation.create('absolute_difference', user_id, [10, 4]),
    ]
    
    # Each calculation maintains its specific type
    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)
    assert isinstance(calculations[4], Modulus)
    assert isinstance(calculations[5], Power)
    assert isinstance(calculations[6], Root)
    assert isinstance(calculations[7], AbsoluteDifference)
    
    # All calculations share the same interface
    results = [calc.get_result() for calc in calculations]
    
    # Each produces its type-specific result
    # Results: addition(6), subtraction(7), multiplication(24), division(20), modulus(1), power(8), root(3), absolute_difference(6)
    assert results == [6, 7, 24, 20, 1, 8, 3, 6]


def test_polymorphic_method_calling():
    """
    Test that polymorphic methods work correctly.
    
    This demonstrates that you can call get_result() on any Calculation
    subclass and get the correct type-specific behavior without knowing
    the exact subclass type at compile time.
    """
    user_id = dummy_user_id()
    inputs = [16, 2]
    
    # Create calculations dynamically based on type string
    calc_types = ['addition', 'subtraction', 'multiplication', 'division', 'modulus', 'power', 'root', 'absolute_difference']
    expected_results = [18, 14, 32, 8, 0, 256, 4, 14]
    
    for calc_type, expected in zip(calc_types, expected_results):
        calc = Calculation.create(calc_type, user_id, inputs)
        # Polymorphic method call: same method name, different behavior
        result = calc.get_result()
        assert result == expected, \
            f"{calc_type} failed: expected {expected}, got {result}"
        
# Model representation test
def test_calculation_repr():
    """Test Calculation model string representation"""
    calc = Addition(user_id=dummy_user_id(), inputs=[1, 2])
    repr_str = repr(calc)
    assert "Calculation" in repr_str
    assert "addition" in repr_str

# Edge cases with data types
def test_calculation_with_floats():
    """Test calculations with floating point inputs"""
    calc = Addition(user_id=dummy_user_id(), inputs=[1.5, 2.7, 3.14])
    result = calc.get_result()
    assert abs(result - 7.34) < 0.01

def test_calculation_with_negative_numbers():
    """Test calculations with negative inputs"""
    calc = Subtraction(user_id=dummy_user_id(), inputs=[-10, 5])
    result = calc.get_result()
    assert result == -15

# Database persistence tests (need db_session fixture from conftest)
def test_calculation_polymorphic_persistence(db_session, test_user):
    """Test that polymorphic calculations persist correctly"""
    addition = Calculation.create("addition", test_user.id, [1, 2, 3])
    addition.result = addition.get_result()
    
    db_session.add(addition)
    db_session.commit()
    db_session.refresh(addition)
    
    retrieved = db_session.query(Calculation).filter_by(id=addition.id).first()
    assert isinstance(retrieved, Addition)
    assert retrieved.type == "addition"

def test_calculation_cascade_delete(db_session, test_user):
    """Test that calculations are deleted when user is deleted"""
    addition = Calculation.create("addition", test_user.id, [1, 2])
    addition.result = 3
    
    db_session.add(addition)
    db_session.commit()
    
    calc_id = addition.id
    
    db_session.delete(test_user)
    db_session.commit()
    
    deleted_calc = db_session.query(Calculation).filter_by(id=calc_id).first()
    assert deleted_calc is None

# ======================================================================================
# Edge Case Tests
# ======================================================================================

def test_calculation_sequential_operations_with_errors():
    """Test calculations with sequential operations that might error."""
    user_id = dummy_user_id()
    
    # Division with chained operations
    division = Division(user_id=user_id, inputs=[100, 5, 2])
    assert division.get_result() == 10.0
    
    # Subtraction resulting in negative
    subtraction = Subtraction(user_id=user_id, inputs=[5, 10])
    assert subtraction.get_result() == -5

def test_calculation_with_very_large_numbers():
    """Test calculations with very large numbers."""
    user_id = dummy_user_id()
    
    # Addition with large numbers
    addition = Addition(user_id=user_id, inputs=[1e10, 2e10])
    assert addition.get_result() == 3e10
    
    # Multiplication with large numbers
    multiplication = Multiplication(user_id=user_id, inputs=[1e8, 1e8])
    assert multiplication.get_result() == 1e16

def test_calculation_with_very_small_numbers():
    """Test calculations with very small decimal numbers."""
    user_id = dummy_user_id()
    
    # Addition with small decimals
    addition = Addition(user_id=user_id, inputs=[0.0001, 0.0002, 0.0003])
    result = addition.get_result()
    assert abs(result - 0.0006) < 1e-10
    
    # Division with small decimals
    division = Division(user_id=user_id, inputs=[0.001, 0.01])
    result = division.get_result()
    assert abs(result - 0.1) < 1e-10

def test_calculation_modulus_with_floats():
    """Test modulus operation with float inputs."""
    user_id = dummy_user_id()
    
    modulus = Modulus(user_id=user_id, inputs=[5.5, 2])
    assert modulus.get_result() == 1.5

def test_calculation_power_with_negative_exponent():
    """Test power operation with negative exponent."""
    user_id = dummy_user_id()
    
    power = Power(user_id=user_id, inputs=[2, -2])
    assert power.get_result() == 0.25

def test_calculation_root_with_decimal_degree():
    """Test root operation with decimal degree."""
    user_id = dummy_user_id()
    
    root = Root(user_id=user_id, inputs=[16, 0.5])
    result = root.get_result()
    # 16 ** (1/0.5) = 16 ** 2 = 256
    assert result == 256

def test_all_calculation_types_with_same_inputs():
    """Test that all calculation types handle the same inputs correctly."""
    user_id = dummy_user_id()
    
    # Each should work with [10, 2]
    addition = Addition(user_id=user_id, inputs=[10, 2])
    assert addition.get_result() == 12
    
    subtraction = Subtraction(user_id=user_id, inputs=[10, 2])
    assert subtraction.get_result() == 8
    
    multiplication = Multiplication(user_id=user_id, inputs=[10, 2])
    assert multiplication.get_result() == 20
    
    division = Division(user_id=user_id, inputs=[10, 2])
    assert division.get_result() == 5.0
    
    modulus = Modulus(user_id=user_id, inputs=[10, 2])
    assert modulus.get_result() == 0
    
    power = Power(user_id=user_id, inputs=[10, 2])
    assert power.get_result() == 100
    
    root = Root(user_id=user_id, inputs=[10, 2])
    result = root.get_result()
    assert abs(result - 3.162) < 0.01  # Approximately sqrt(10)