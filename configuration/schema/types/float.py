from typing import Any

from .type import Type


class Float(Type):
    """
    A schema type representing a float value.
    This type validates that the input is a floating-point number (float).
    
    Parameters
    ----------
    min_value : Optional[`float`]
        Minimum value allowed. Default is None.
    max_value : Optional[`float`]
        Maximum value allowed. Default is None.
    min_precision : Optional[`int`]
        The minimum number of decimal places allowed. Default is None.
    max_precision : Optional[`int`]
        The maximum number of decimal places allowed. Default is None.

    Example
    -------
    **example.yml**
    ```
    rate: 0.75
    price: 19.99
    item_id: 10
    ```
    
    **your_schema.py**
    ```python
    class YourSchema(ConfigSchema):
        rate = Float(min_precision=3) # Fail (2 < 3)
        price = Float(min_value=10.15, max_value=20) # Pass
        item_id = Float() # Pass
    ```
    """
    
    def __init__(
        self, 
        min_value: float = None,
        max_value: float = None,
        min_precision: int = None,
        max_precision: int = None
    ) -> None:
        
        self.min_value = min_value
        self.max_value = max_value
        self.min_precision = min_precision
        self.max_precision = max_precision
    
    def __call__(self, value: Any) -> None:
        
        # Check if the value is a float, raise TypeError if not
        if not isinstance(value, float):
            raise TypeError(f"Expected a float, but got {type(value).__name__}")
        
        # Check if the value meets the minimum value constraint
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value is too small. Minimum allowed value is {self.min_value}.")
        
        # Check if the value meets the maximum value constraint
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value is too large. Maximum allowed value is {self.max_value}.")
        
        # Check the precision (number of decimal places)
        str_value = str(value)
        decimal_places = len(str_value.split(".")[1]) if "." in str_value else 0
        
        # Validate min precision
        if self.min_precision is not None and decimal_places < self.min_precision:
            raise ValueError(f"Value has insufficient precision. Minimum allowed precision is {self.min_precision} decimal places.")
        
        # Validate max precision
        if self.max_precision is not None and decimal_places > self.max_precision:
            raise ValueError(f"Value exceeds allowed precision. Maximum allowed precision is {self.max_precision} decimal places.")