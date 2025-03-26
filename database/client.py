import abc
import inspect

from typing_extensions import Self


class Client(abc.ABC):
    """
    A base class for database clients.
    All clients must inherit from this class and implement the abstract methods.
    """
    
    def __init__(self, connection):
        self.conn = connection
        
    """Override Methods"""
    
    @classmethod
    @abc.abstractmethod
    def connect(cls, *args, **kwargs) -> Self:
        """
        Establishes a connection to the database.

        Returns
        -------
        Self[Client]
            An instance of the client with an active connection.
        """
        return cls()
    
    @abc.abstractmethod
    def close(self, *args, **kwargs) -> None:
        """Closes the connection to the database."""
        pass
    
    """Backend Methods"""
    
    @classmethod
    def is_async(cls) -> bool:
        """
        Determain if the client use asynchronus methods.

        Returns
        -------
        bool
            True if the `connect` method is asynchronous, otherwise False.
        """
        return inspect.iscoroutinefunction(cls.connect)
    
    def is_connected(self):
        """
        Checks if the client is connected to the database.

        Returns
        -------
        bool
            True if the connection is active, otherwise False.
        """
        return self.conn is not None