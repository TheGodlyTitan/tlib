import re
from typing import (
    Any,
    Optional
)

from .type import Type


class String(Type):
    """
    A schema value type representing a string.
    
    Parameters
    ----------
    min_length : `int`
        fill desc
    max_length : `int`
        fill desc
    regex : `str`
        fill desc
        
    Example
    -------
    **example.yml**
    ```
    username: "my_user"
    password: "secret123"
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        username = String(min_length=3, max_length=20) # Pass
        password = String(min_length=10) # Fail (9 < 10)
    ```
    """
    def __init__(
        self, 
        min_length: Optional[int] = None, 
        max_length: Optional[int] = None, 
        regex: Optional[str] = None
    ) -> None:
        
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex

    def __call__(self, value: Any) -> None: 
        
        # Check if the value is a string.
        if not isinstance(value, str):
            raise TypeError(f"Expected a string, but got {type(value).__name__}")

        # Check if the value meets the minimum length requirement
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"String is too short. Minimum length is {self.min_length}.")

        # Check if the value exceeds the maximum length requirement
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"String is too long. Maximum length is {self.max_length}.")

        # Check if the value matches the regular expression, if specified
        if self.regex is not None:
            if not re.match(self.regex, value):
                raise ValueError(f"String does not match the required pattern: {self.regex}")