from typing import Any, Optional

from .type import Type


class Array(Type):
    """
    A schema type representing an array of values with a homogeneous type.
    
    Parameters
    ----------
    type : `Type`
        The type of every element in the array.
    min_length : `int`, optional
        The minimum number of elements the array should have.
    max_length : `int`, optional
        The maximum number of elements the array should have.
    unique_elements : `bool`, optional
        Whether the array should have unique elements.
    
    Example
    -------
    **example.yml**
    ```
    fruits:
        - "Apple"
        - "Orange"
        - "Banana"
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        fruits = Array(String())
    ```
    """
    def __init__(
        self, 
        type: Type, 
        max_length: int = None, 
        min_length: int = None,
        unique_elements: bool = False,
    ) -> None:
        
        self.type = type
        self.max_length = max_length
        self.min_length = min_length
        self.unique_elements = unique_elements
        
    def __call__(self, value: Any) -> None:
        
        # Validate if the value is a list
        if not isinstance(value, list):
            raise TypeError(f"Expected a list, but got {type(value).__name__}")

        # Validate the length constraints
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"Array is too short. Minimum length is {self.min_length}.")
        
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Array is too long. Maximum length is {self.max_length}.")

        # Validate elements
        for idx, element in enumerate(value):
            # Check the type of each element
            self.type(element)
        
        # Validate uniqueness of elements
        if self.unique_elements and len(value) != len(set(value)):
            raise ValueError("Array elements are not unique.")
        
    