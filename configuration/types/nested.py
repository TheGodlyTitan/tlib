from typing import (
    Any,
    Dict,
    Tuple
)

from .type import Type


class Nested(Type):
    """
    A schema type representing a nested key-value structure.
    Where each argument should be a tuple containing a key name (str) and a type.
    Combine with other `Nested` typings for multi-nested configurations.
    
    Parameters
    ----------
    *args : Tuple[str, Type]
        A variable number of tuples, where each tuple contains:
        - key name (str): The key in the dictionary.
        - expected type (Type): The expected type for the value of the key.
    
    Example
    -------
    **example.yml**
    ```
    settings:
        max_users: 100
        owner_id: "123"
        
    log_settings:
        debug_mode: true
        handlers:
            is_enabled: true     
    ```

    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        settings = Nested( # Pass
            ('max_users', Integer()),
            ('owner_id', String()),
        )
        log_settings = Nested( # Pass
            ('debug_mode', Boolean()),
            ('handlers', Nested(
                ('is_enabled', Boolean())
            ))  
        )
    ```
    """
    def __init__(self, *args: Tuple[str, Type]) -> None:
        self.args = args
        
    def check(self, value: Dict[str, Any]):
        for key, expected_type in self.args:
            
            if key not in value:
                raise ValueError(f"Missing key: {key}")
            
            # Check that the value matches the expected type by calling the type instance
            expected_type.check(value[key])
        