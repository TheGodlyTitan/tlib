from abc import ABC, abstractmethod
from typing import Any


class Type(ABC):
    """
    Base class for all schema types.
    
    Example
    -------
    A simple restriction to only allow a given number.
    ```
    class IsNumber(Type):
    
        def __init__(self, number: int) -> None:
            self.number = number
            
        def __call__(self, value) -> None:
        
            if not isinstance(value, int):
                raise TypeError(f'Expected a nunmber, but got {type(value).__name__}')
                
            if value != self.number:
                raise ValueError(f'Value must be number: {self.number}')
    ```
    """
    
    @abstractmethod
    def __call__(self, value: Any) -> None:
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
