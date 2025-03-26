import json
import pathlib

from tlib.configuration import (
    errors,
    ConfigurationData,
)
from .parser import ConfigParser


class JSONParser(ConfigParser):
    """
    A `ConfigParser` subclass to handle `.json` configurations.
    """
    def parse(source: pathlib.Path) -> ConfigurationData:
        """"
        Parses configuration from a JSON file and returns it as a dictionary.
        
        Parameters
        ----------
        source : `Path`
            The file path to the JSON configuration file.
        
        Returns
        -------
        `Dict[str, Any]`
            A dictionary containing the configuration values.
        
        Raises
        ------
        ConfigParsingError
            If the file is malformed or contains syntax errors.
        ConfigError
            If the file cannot be accessed or read.
        """
        try:
            
            with source.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        
        except json.JSONDecodeError as e:
            raise errors.ConfigParsingError(source, f"Invalid JSON format: {e}")
        
        except (OSError, IOError) as e:
            raise errors.ConfigError(f"Failed to open {source}: {e}")