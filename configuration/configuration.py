import pathlib
from typing import Any

from .data import ConfigurationData



class Configuration:
    """
    A class that represents a configuration with key-value pairs.

    This class is used to encapsulate configuration data loaded from various sources, such as 
    environment variables, JSON files, YAML files, etc. The key-value pairs are stored as 
    instance attributes, and the class provides methods to retrieve these values or convert 
    the data back into a dictionary.
    """
    def __init__(self, data: ConfigurationData, path: pathlib.Path = None):
        
        self.__data = data
        self.__path = path
        
        for key, value in data.items():
            if isinstance(value, dict):
                value = Configuration(value)
            setattr(self, key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by key.

        Parameters
        ----------
        key : str
            The key of the configuration value, 
            which can be a nested key (e.g., "settings.max_users")
        default : Any, optional
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The value associated with the key or the default value.
        """
        keys = key.split('.')
        value = self.__data
        
        for k in keys:
            
            value = value.get(k, default) if isinstance(value, dict) else default
            
            if value == default:
                break
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Sets a configuration value by key.
        
        Parameters
        ----------
        key : str
            The key of the configuration value.
        value : Any
            The value to set for the given key.
            
        Raises
        ------
        ConfigurationRestrictedError
            if `cls.CAN_MODIFY` is set to `False`; disabling configuration changes.
        """        
        keys = key.split('.')
        data = self.__data
        
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value
        setattr(self, keys[-1], Configuration(value) if isinstance(value, dict) else value)
    
    def to_dict(self) -> ConfigurationData:
        """
        Converts the configuration instance back into a dictionary, handling nested configurations.

        Returns
        -------
        ConfigurationData
            A dictionary representation of the configuration, including any nested configurations.
        """
        return self.__data
        
    def __eq__(self, other: object) -> bool:
        """
        Compare the configuration with another dictionary or Configuration object.
        """
        if isinstance(other, Configuration):
            return self.__data == other.__data
        if isinstance(other, dict):
            return self.__data == other
        return False
