import json
import pathlib
from typing import Dict, Any

from configuration import (
    errors,
    Parser,
)


class JSONParser(Parser):
    """
    A `Parser` subclass to handle `.json` configurations.
    """
    def parse(file: pathlib.Path) -> Dict[str, Any]:
        """"
        Parses configuration from a JSON file and returns it as a dictionary.
        
        Parameters
        ----------
        file : `Path`
            The file path to the JSON configuration file.
        
        Returns
        -------
        `Dict[str, Any]`
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
                data = json.load(file)
            return data
        
        except json.JSONDecodeError as e:
            raise errors.ParsingError(file, str(e))
        
        except (OSError, IOError) as e:
            raise errors.SourceError(file, e)