import yaml
import pathlib

from tlib.configuration import (
    errors,
    ConfigurationData,
)
from .parser import ConfigParser


class YAMLParser(ConfigParser):
    """
    A `Parser` subclass to handle `.yml`/`.yaml` configurations.
    """
    def parse(source: pathlib.Path) -> ConfigurationData:
        """
        Parses configuration from a .yml (YAML) file and returns it as a dictionary.
        
        Parameters
        ----------
        source : `Path`
            The file path to the .yml file.
        
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
            
            with source.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                
            # If YAML is incorrectly parsed as a string instead of a dictionary
            if not isinstance(data, dict):
                raise errors.ConfigParsingError(source, "YAML file contains invalid structure.")
            
            return data
        
        except yaml.YAMLError as e:
            raise errors.ConfigParsingError(source, str(e))
        
        except (OSError, IOError) as e:
            raise errors.ConfigError(f"Failed to open {source}: {e}")


YMLParser = YAMLParser