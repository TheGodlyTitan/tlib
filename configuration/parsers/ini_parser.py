import pathlib
import configparser
from typing import Dict, Any

from configuration import (
    errors,
    Parser,
)


def _convert(value: str) -> Any:
    """
    Converts values to their appropriate types (int, float, bool, None).
    """
    # Check for empty string and return None
    value = value or None
    if not value:
        return value
    
    # Check if the value is inside quotes (i.e., a forced string)
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]  # Strip the surrounding quotes and return as string
    
    # Try converting to boolean
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    
    # Try converting to integer if not quoted
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try converting to float if not quoted
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return the string if no conversion was possible
    return value
        
class INIParser(Parser):
    """
    A `Parser` subclass to handle `.ini` configurations.
    
    By default .ini files contain all values as strings, therefore this loader
    contains methods to convert string values into their appropriate types.
    You can force any value to remain a string using "" around the value for instance,
    "1.0" will remain a string, as well as "False" (Truthy str).
    
    Conversions
    -----------
     - Strings: Values are treated as strings by default.
     - Strings: Values that cannot be converted to `bool`, `int`, or `float` remain as strings.
     - Booleans: Values like `true` or `false` (case-insensitive) are converted to Python `True` or `False`.
     - Integers: Values that represent integers (like `100`) are converted to Python `int` type.
     - Floats: Values that represent floating-point numbers (like `15.5`) are converted to Python `float` type.
     - None: Missing values for a key are assigned `None`
    
    Example
    -------
    **Input**:
    ```
    [general]
    app_name = TestApp
    version = "1.0"
    is_enabled = true
    is_active = "true"
    
    [settings]
    max_users = 100
    timeout = 15.5
    debug_mode = 
    ```
    
    **Output:**
    ```python
    {
        "general": {
            "app_name": "TestApp",
            "version": "1.0",      # Forced String 
            "is_enabled": True,
            "is_active": "true"    # Forced String
        },
        "settings": {
            "max_users": 100,
            "timeout": 15.5,
            "debug_mode": None     # Empty Value
        }
    }
    ```
    """
    
    def parse(file: pathlib.Path) -> Dict[str, Any]:
        """
        Parses configuration from an INI or CFG file and returns it as a dictionary.

        Parameters
        ----------
        file : Path
            The file path to the INI or CFG configuration file.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the configuration values.

        Raises
        ------
        ParsingError
            The file fails to parse due to file syntax errors.
        SourceError
            If the source file failed to open.
        """
        
        parser = configparser.ConfigParser()
        
        try:
            with file.open("r", encoding="utf-8") as file:
                parser.read_file(file)

            data = {
                section: {
                    key: _convert(value)
                    for key, value in parser.items(section)
                }
                for section in parser.sections()
            }
                    
            return data
        
        except configparser.Error as e:
            raise errors.ParsingError(file, str(e))
        
        except (OSError, IOError) as e:
            raise errors.SourceError(file, e)
        

CFGParser = INIParser