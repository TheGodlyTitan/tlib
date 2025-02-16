from typing import Any

from .type import Type


class OneOf(Type):
    """
    A schema type that allows a value to be one of multiple specified types.

    This type validates that the input matches at least one of the provided types.
    
    Parameters
    ----------
    *types : Type
        The types that are allowed for the value.

    Example
    -------
    **example.yml**
    ```
    app_version: 2
    setting_name: "high"
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        app_version = OneOf(Integer(), String())  # Accepts either int or str
        setting_name = OneOf(String(), Boolean()) # Accepts str or bool
    ```
    """
    def __init__(self, *types: Type) -> None:
        if not types:
            raise ValueError("OneOf must have at least one type specified.")
        self.types = types
        
    def __call__(self, value: Any) -> None:
        for expected_type in self.types:
            try:
                expected_type(value)  # Try each type validator
                return  # If one succeeds, validation passes
            except (TypeError, ValueError):
                continue  # Try the next type

        # If none of the types pass, raise an error
        allowed_types = ", ".join(type_.__class__.__name__ for type_ in self.types)
        raise TypeError(f"Expected one of ({allowed_types}), but got {type(value).__name__}")