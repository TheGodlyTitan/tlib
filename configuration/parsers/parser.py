import abc
import pathlib

from tlib.config import ConfigurationData


class ConfigParser(abc.ABC):
    """
    A base class for configuration parsers.
    All parsers must inherit from this class and implement the `parse` method.
    """
    
    @staticmethod
    @abc.abstractmethod
    def parse(source: pathlib.Path) -> ConfigurationData:
        """
        Load configuration data from the given source.

        Parameters
        ----------
        source : Union[str, Path]
            The path to the configuration file.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the configuration data.
        """
        pass
    
