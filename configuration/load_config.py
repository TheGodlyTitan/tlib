import os
import pathlib
from typing import Optional

from .errors import *
from .parsers import *
from .schema import Schema
from .configuration import Configuration 


def load_config(
    path: os.PathLike, 
    parser: Parser = None, 
    schema: Schema = None
) -> Configuration:
    """
    Loads a configuration from a specified source path and converts it into a `Configuration` class.
    
    Parameters
    ----------
    path : PathLike
        The file path or environment variable to load.
    parser : Optional[Parser]
        An optional parser class to handle custom configuration formats.
    schema : Optional[Schema]
        An optional schema class to handle configuration key/value validation.
        
    Returns
    -------
    Configuration
        An instance of the Configuration class with the loaded values.
    
    Raises
    ------
    FileNotFoundError
        If the source file does not exist.
    TypeError
        If the source file type is unsupported.
    ValidationError
        If the source data does not match the schema (If given).
    """
    
    # Convert source to Path object if it's a string
    if isinstance(path, str):
        path = pathlib.Path(path)
    
    # Ensure the configuration file exists
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    # Parse the data from the source file.
    # Uses given parser if supplied, otherwise uses built-in parser.
    if parser:
        data = parser.parse(path)
    else:
        # Determine source type based on file extension
        match path.suffix.lower():
            case ".yaml" | ".yml":
                data = YAMLParser.parse(path)
            case ".json":
                data = JSONParser.parse(path)         
            case ".ini":
                data = INIParser.parse(path)           
            case ".cfg":
                data = CFGParser.parse(path)           
            case ".toml":
                data = TOMLParser.parse(path)          
            case _:
                # Requires end-user to create custom `Parser`.
                raise SourceError(path, "File type not natively supported.")

    # Check the source datas values based on the schema (if any).
    if schema:
        schema._validate(data)

    return Configuration(data, path)



