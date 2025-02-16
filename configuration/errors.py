import pathlib


class ConfigError(Exception):
    """
    Base exception for all `configuration` library errors.
    """
    pass


class FileTypeError(ConfigError):
    """
    Raised when the configuration file format is not natively supported.
    Use custom `ConfigParser` classes to parse non-native file types.
    """
    def __init__(self, path: pathlib.Path):
        super().__init__(f"Unsupported configuration format: {path}")

    
class ConfigParsingError(ConfigError):
    """
    Raised when a configuration file cannot be parsed due to syntax errors or malformed content.
    """
    def __init__(self, path: pathlib.Path, message: str):
        super().__init__(f"Failed to parse configuration file {path}: {message}")
        

class ConfigValidationError(ConfigError):
    """
    Raised when a configuartion file fails to validate from the schema.
    """
    def __init__(self, message: str, key: str, error: Exception = None) -> None:
        super().__init__(f"{message} for key '{key}': {error}")
