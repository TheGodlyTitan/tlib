import toml
import pathlib

from tlib.config import (
    errors,
    ConfigurationData,
)
from .parser import ConfigParser


class TOMLParser(ConfigParser):
    """
    A `Parser` subclass to handle `.toml` configurations.
    """
    def parse(source: pathlib.Path) -> ConfigurationData:
        """
        Parses configuration from a .toml (TOML) file and returns it as a dictionary.
    
        Parameters
        ----------
        source : `Path`
            The file path to the .toml configuration file.
        
        Returns
        -------
        `Dict[str, Any]`
            A dictionary containing the configuration values.
        
        Raises
        ------
        ConfigurationSyntaxError
            If the file is malformed or contains syntax errors.
        ConfigurationError
            If the file cannot be accessed or read.
        """
    
        try:
            data = toml.load(source)
            return data

        except toml.TomlDecodeError as e:
            raise errors.ConfigParsingError(source, str(e))
        
        except (OSError, IOError) as e:
            raise errors.ConfigError(f"Failed to open {source}: {e}")
        