import os
import dotenv
import pathlib

from tlib.configuration import (
    errors,
    ConfigurationData,
)
from .parser import ConfigParser


class ENVParser(ConfigParser):
    """
    A `ConfigParser` subclass to handle `.env` configuration files.
    """

    def parse(source: pathlib.Path) -> ConfigurationData:
        """
        Parses configuration from an .env file and returns it as a dictionary.

        Parameters
        ----------
        source : Path
            The file path to the .env configuration file.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the configuration values.

        Raises
        ------
        ConfigParsingError
            If the file contains syntax errors.
        ConfigError
            If the file cannot be accessed or read.
        """
        
        # Load environment variables from the .env file
        if not dotenv.load_dotenv(dotenv_path=source):
            raise errors.ConfigParsingError("Failed to load environment variables from .env file.")
        
        # Collect environment variables, replacing empty strings with None
        try:
            
            data = {
                key: (value if value.strip() else None) for key, value in os.environ.items()
            }
            return data
    
        except Exception as e:
            raise errors.ConfigError(source, str(e))
        