import os
import pathlib
from typing import Optional

from .data import ConfigurationData
from .errors import *
from .parsers import *
from .schema import ConfigSchema
from .configuration import Configuration 


__all__ = (
    'load_config'
)

data: ConfigurationData


def load_config(
    source: os.PathLike = '.env', 
    parser: Optional[ConfigParser] = None, 
    schema: Optional[ConfigSchema] = None
) -> Configuration:
    """
    Loads a configuration from a specified source and converts it into a Configuration class.
    
    Parameters
    ----------
    source : PathLike
        The file path or environment variable to load.
    parser : Optional[ConfigParser]
        An optional parser class to handle custom configuration formats.
    schema : Optional[ConfigSchema]
        An optional schema class to handle configuration key/value validation.
        
    Returns
    -------
    Configuration
        An instance of the Configuration class with the loaded values.
    
    Raises
    ------
    FileNotFoundError
        If the source file does not exist.
    FileTypeError
        If the source file type is unsupported.
    ConfigValidationError
        If the source data does not match the schema
    """
    
    # Convert source to Path object if it's a string
    if isinstance(source, str):
        source = pathlib.Path(source)
    
    # Ensure the configuration file exists
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"Configuration file not found: {source}")
    
    # Use custom parser if provided
    if parser:
        data = parser.parse(source)
        schema._validate(data) if schema else None
        return Configuration(data, source)
    
    # Determine source type based on file extension
    match source.suffix.lower():
        
        case ".env":
            data = ENVParser.parse(source)
            
        case ".yaml" | ".yml":
            data = YAMLParser.parse(source) # YMLParser.parse(source)

        case ".json":
            data = JSONParser.parse(source)
        
        case ".ini":
            data = INIParser.parse(source)
        
        case ".cfg":
            data = CFGParser.parse(source)
        
        case ".toml":
            data = TOMLParser.parse(source)
        
        case _:
            raise FileTypeError(source)
    
    schema._validate(data) if schema else None
    return Configuration(data, source)



