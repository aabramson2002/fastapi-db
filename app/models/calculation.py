#calculation model
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional, Dict, Any

from sqlalchemy import Column, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from app.database import Base #using Base from database instead of from sqlalchemy.orm to avoid circular imports

#defines all of the data fields
class Calculation(Base):
    __tablename__ = 'calculations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False) # "addition", "subtraction", "multiplication", "division", and more
    inputs = Column(JSON, nullable=False) # Store inputs as JSON array of floats
    #operation_a = Column(Float, nullable=False)
    #operation_b = Column(Float, nullable=False)
    result = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with User
    """Calculation class connects back to the user"""
    user = relationship("User", back_populates="calculations")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "calculation",
    }

    @classmethod
    def create(cls, calculation_type: str, user_id: uuid.UUID, inputs: list[float]) -> "Calculation":
        """Factory method to create a Calculation instance based on the type of calculation."""
        calculation_classes = {
            "addition": Addition,
            "subtraction": Subtraction,
            "multiplication": Multiplication,
            "division": Division,
        }
        calculation_class = calculation_classes.get(calculation_type.lower())
        if not calculation_class:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calculation_class(user_id=user_id, inputs=inputs)
    
    @abstractmethod
    def get_result(self) -> float:
        """Abstract method to calculate the result of the operation."""
        raise NotImplementedError

    def __repr__(self):
        return f"<Calculation(type='{self.type}', inputs={self.inputs}, result={self.result})>"
    
    
class Addition(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "addition",
    }

    def get_result(self) -> float:
        """
        Calculate the sum of all input numbers.
        
        Returns:
            The sum of all inputs
            
        Raises:
            ValueError: If inputs is not a list or has fewer than 2 numbers
        """
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError(
                "Inputs must be a list with at least two numbers."
            )
        return sum(self.inputs)

class Subtraction(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "subtraction",
    }

    def get_result(self) -> float:
        """
        Calculate the difference of all input numbers.
        
        Returns:
            The difference of all inputs
            
        Raises:
            ValueError: If inputs is not a list or has fewer than 2 numbers
        """
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError(
                "Inputs must be a list with at least two numbers."
            )
        result = self.inputs[0]
        for num in self.inputs[1:]:
            result -= num
        return result

class Multiplication(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "multiplication",
    }

    def get_result(self) -> float:
        """
        Calculate the product of all input numbers.

        Returns:
            The product of all inputs

        Raises:
            ValueError: If inputs is not a list or has fewer than 2 numbers
        """
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError(
                "Inputs must be a list with at least two numbers."
            )
        result = 1
        for num in self.inputs:
            result *= num
        return result


class Division(Calculation):
    __mapper_args__ = {
        "polymorphic_identity": "division",
    }

    def get_result(self) -> float:
        """
        Calculate the quotient of all input numbers.

        Returns:
            The quotient of all inputs

        Raises:
            ValueError: If inputs is not a list or has fewer than 2 numbers
        """
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError(
                "Inputs must be a list with at least two numbers."
            )
        result = self.inputs[0]
        for num in self.inputs[1:]:
            try:
                result /= num
            except ZeroDivisionError:
                raise ValueError("Cannot divide by zero.")
        return result
    
        
