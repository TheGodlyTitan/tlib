from abc import ABC, abstractmethod
from typing import Any


class Type(ABC):
    """
    Base class for all schema types.
    
    Example
    -------
    A simple schema type that only accept a specific number value.
    ```
    class SpecificInteger(Type):
    
        def __init__(self, integer: int) -> None:
            self.integer = integer
            
        def check(self, value: Any) -> None:
        
            if not isinstance(value, int):
                raise TypeError(f'Expected integer, but got {type(value).__name__}')
                
            if value != self.integer:
                raise ValueError(f'Integer must be {self.integer}, but got {value}')
    ```
    """
    
    @abstractmethod
    def check(self, value: Any) -> None:
        """
        Validate the given value.

        Parameters
        ----------
        value : `Any`
            The value to check.
        
        Raises
        ------
        TypeError
            If the value is not of the expected type.
        ValueError
            If the value does not pass the restrictions (e.g., min_length).
        """
        pass
