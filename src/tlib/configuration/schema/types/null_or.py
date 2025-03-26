from typing import Any

from .type import Type


class NullOr(Type):
    """
    A schema type representing a value that can either be `None` or one of the specified types.
    This can be combed with other library types for more complex validation.
    
    Parameters
    ----------
    types : Type
        One or more types to be validated against. The value must be one of these types, or `None`.
        
    Example
    -------
    **example.yml**
    ```
    debug_mode: true
    version: 2
    app_id: "123123"
    ```

    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        debug_mode = NullOr(Boolean()) # Pass
        version = NullOr(String()) # Fail (2 is Integer)
        app_id = NullOr(String(), Integer()) # Pass
    ```
    """
    def __init__(self, *types: Type):
        if not types:
            raise ValueError("NullOr must have at least one type specified.")
        self.types = types
        
    def __call__(self, value: Any) -> None:
        
        # Check if the value is None (allowed by this type)
        if value is None:
            return True

        # Check if the value matches one of the provided types
        for _type in self.types:
            
            try:
                _type(value)  # Try to validate with the provided type
                return
            except (TypeError, ValueError):
                continue  # If the type fails, try the next type

        # If the value didn't match any allowed types, raise TypeError
        raise TypeError(f"Expected None or one of the following types: {', '.join([t.__class__.__name__ for t in self.types])}, but got {type(value).__name__}.")