import pathlib


class Error(Exception):
    """
    Base exception for all `configuration` module errors.
    """
    pass

class SourceError(Error):
    """
    Raised when a configuration file (source) fails to open or is unsupported.
    """
    def __init__(self, path: pathlib.Path, exception: Exception):
        super().__init__(f"Configuration source failed to open '{path}': {exception}")
   
        
class ParsingError(Error):
    """
    Raised when a configuration file fails to parse due to incorrect syntax or malformed content.
    """
    def __init__(self, path: pathlib.Path, message: str):
        super().__init__(f"Failed to parse configuration file {path}: {message}")
        

class ValidationError(Error):
    """
    Raised when a configuration file failes the validation of a schema.
    """
    def __init__(self, message: str, key: str, error: Exception = None) -> None:
        super().__init__(f"{message} for key '{key}': {error}")