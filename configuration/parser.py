import abc
import pathlib
from typing import Dict, Any


class Parser(abc.ABC):
    """
    A base class for configuration parsers.
    All parsers must inherit from this class and implement the `parse` method.
    """
    
    @staticmethod
    @abc.abstractmethod
    def parse(file: pathlib.Path) -> Dict[str, Any]:
        """
        Load configuration data from the given source.

        Parameters
        ----------
        file : Union[str, Path]
            The path to the configuration file.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the configuration data.
        """
        pass
    