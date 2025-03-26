import os
from typing import Any

from .type import Type


class Filepath(Type):
    """
    A schema type that validates whether a string is a valid file path, which can 
    be either a file or a directory. Additionally, it allows enforcement of a specific
    file extension.
    
    Parameters
    ----------
    exists : Optional[`bool`]
        If True, ensures the file at the given path exists.
    file_extension : Optional[`str`]
        Ensures the file has the given extension (e.g., `.cfg`). Defaults to None (any extension).
        
    Example
    -------
    **example.yml**
    ```
    filepath_one: "path/to/file.yml"
    filepath_two: "path/to/other.cfg"
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        filepath_one = Filepath(exists=True, extension='.yml') # Pass
        filepath_two = Filepath(exists=True, extension='.yml') # Fail (extension='.cfg')
    ```
    """
    
    def __init__(
        self,
        exists: bool = None,
        file_extension: str = None
    ) -> None:
        
        self.exists = exists
        self.file_extension = file_extension

        
    def __call__(self, value: Any) -> None:

        # Ensure the value is a string
        if not isinstance(value, str):
            raise TypeError(f"Expected a string path, but got {type(value).__name__}")
        
        # Check if the path exists (if 'exists' is True)
        if self.exists and not os.path.exists(value):
            raise ValueError(f"Path at {value} does not exist.")
        
        # Check the file extension (if 'file_extension' is provided)
        if self.file_extension and not value.endswith(self.file_extension):
            raise ValueError(f"File at {value} does not have the expected extension {self.file_extension}.")