from typing import Any

from .type import Type


class Boolean(Type):
    """
    A schema type representing a boolean value.
    This type validates that the input is a boolean (either True or False).
    
    Parameters
    ----------
    only : bool
        A boolean value that determines if the value is restricted. 
        - If `True`, only `True` is allowed. 
        - If `False`, only `False` is allowed. 
        - If `None`, both `True` and `False` are allowed.
        
    Example
    -------
    **example.yml**
    ```
    debug_mode: true
    is_enabled: true
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        debug_mode = Boolean() # Pass
        is_enabled = Boolean(False) # Fail (Only False)
    ```
    """
    def __init__(
        self, 
        only: bool = None
    ) -> None:
        
        self.only = only
        
    def __call__(self, value: Any) -> None:
        
        # Check if the value is a boolean, raise TypeError if not
        if not isinstance(value, bool):
            raise TypeError(f"Expected a boolean, but got {type(value).__name__}")
        
        # If `only` is set to True, the value must be True
        if self.only is True and value is not True:
            raise ValueError("Value must be True.")
        
        # If `only` is set to False, the value must be False
        if self.only is False and value is not False:
            raise ValueError("Value must be False.")
        