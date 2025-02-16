import abc

from tlib.configuration import (
    errors,
    ConfigurationData
)
from .types import Type


class ConfigSchema(abc.ABC):
    """
    A class for defining structured configuration schemas.

    This class is used to define schemas where each attribute is a `Type` instance.
    The `validate` method ensures that a given dictionary adheres to the schema.

    Example
    -------
    **example.yml**
    ```
    app_name: "TestApp"
    settings:
        max_users: 100
        debug_mode: false
    flags:
        - "flag_one"
        - "flag_two"
    ```
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        app_name: String()
        settings: Nested(
            ('debug_mode', Boolean()),
            ('max_users', Integer())
        )
        flags: Array(String())
    ```
    """
    
    @classmethod
    def _validate(cls, data: ConfigurationData) -> None:
        """
        Validates the given configuration dictionary against the schema.

        Parameters
        ----------
        data : Dict[str, Any]
            The dictionary containg the configuration to validate.

        Raises
        ------
        ConfigValidationError:
            If the data fails to validate; does not follow schema structure. 
        """

        key: str
        _type: Type
        
        fields = cls._get_schema_fields()

        for key, _type in fields.items():
            if key not in data:
                raise errors.ConfigValidationError("Missing required field", key)
            
            value = data[key]
            
            try:
                _type(value)  # Validate value
                
            except (TypeError, ValueError) as e:
                raise errors.ConfigValidationError("Invalid value", key, e)
            
    @classmethod
    def _get_schema_fields(cls):
        """
        Extracts schema field definitions from the class dictionary,
        ignoring built-in attributes (__xxx__).
        """
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("__") and isinstance(value, Type)  # Ignore special attributes
        }
