from typing import Any

from .type import Type


class Integer(Type):
    """
    A schema type representing an integer with optional validation rules such as range constraints
    or checks for even/odd numbers.
 
    Example
    -------
    **example.yml**
    ```
    age: 25
    temperature: 76
    wind_speed: 15
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        age = Integer() # Pass
        temperature = Integer(max_value=50) # Fail (76 > 50)
        wind_speed = Integer(min_value=1, max_value=15) # Pass
    ```
    """
    
    def __init__(
        self, 
        min_value: int = None, # Inclusive
        max_value: int = None, # Inclusive
        is_even: bool = None, 
        is_odd: bool = None
    ) -> None:
        
        self.min_value = min_value
        self.max_value = max_value
        self.is_even = is_even
        self.is_odd = is_odd
        
    def check(self, value: Any) -> None:
        
        # Check if the value is a integer.
        if not isinstance(value, int):
            raise TypeError(f"Expected a integer, but got {type(value).__name__}")
        
        # Check if the value meets the minimum requirement
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Integer is too small. Minimum value is {self.min_value}.")
        
        # Check if the value meets the maximum requirement
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Integer is too large. Maximum value is {self.max_value}.")
        
        # Check if the value is required to be even
        if self.is_even and value % 2 != 0:
            raise ValueError(f"Integer must be even, but got {value}.")
        
        # Check if the value is required to be odd
        if self.is_odd and value % 2 == 0:
            raise ValueError(f"Integer must be odd, but got {value}.")
        