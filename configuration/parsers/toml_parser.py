import toml
import pathlib
from typing import Dict, Any

from configuration import (
    errors,
    Parser,
)


class TOMLParser(Parser):
    """
    A `Parser` subclass to handle `.toml` configurations.
    """
    def parse(file: pathlib.Path) -> Dict[str, Any]:
        """
        Parses configuration from a .toml (TOML) file and returns it as a dictionary.
    
        Parameters
        ----------
        file : `Path`
            The file path to the .toml configuration file.
        
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
            data = toml.load(file)
            return data

        except toml.TomlDecodeError as e:
            raise errors.ParsingError(file, str(e))
        
        except (OSError, IOError) as e:
            raise errors.SourceError(file, e)
        