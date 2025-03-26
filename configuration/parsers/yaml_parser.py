import yaml
import pathlib
from typing import Dict, Any

from configuration import (
    errors,
    Parser,
)


class YAMLParser(Parser):
    """
    A `Parser` subclass to handle `.yml`/`.yaml` configurations.
    """
    def parse(file: pathlib.Path) -> Dict[str, Any]:
        """
        Parses configuration from a .yml (YAML) file and returns it as a dictionary.
        
        Parameters
        ----------
        file : `Path`
            The file path to the .yml file.
        
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
    
        try:
            
            with file.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                
            # If YAML is incorrectly parsed as a string instead of a dictionary
            if not isinstance(data, dict):
                raise errors.ParsingError(file, "YAML file contains invalid structure.")
            
            return data
        
        except yaml.YAMLError as e:
            raise errors.ParsingError(file, str(e))
        
        except (OSError, IOError) as e:
            raise errors.SourceError(file, e)


YMLParser = YAMLParser