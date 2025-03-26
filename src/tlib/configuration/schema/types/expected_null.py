from typing import Any


class ExpectedNull(Type):
    """
    A schema type representing an expected `None`/`null` value.
    This type is used to ensure that a key exists but its value must be `None`/`null`.
    
    Example
    -----
    **example.yml**
    ```
    version: null
    app_name: "TestApp"
    ```

    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        version = ExpectedNull() # Pass
        app_name = ExpectedNull() # Fail (is String)
    ```
    """
    def __init__(self) -> None:
        pass
    
    def __call__(self, value: Any) -> bool:
        if value is not None:
            raise ValueError(f"Expected None, but got {type(value).__name__}.")
