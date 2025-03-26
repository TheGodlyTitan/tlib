from typing_extensions import Self

import pymongo

from database import Client
from database.errors import InterfaceError


class MongoClient(Client):
    """
    Synchronous MongoDB database client implementation
    Uses `pymongo` for synchronous database interactions. 
    """
    
    def __init__(self, connection: pymongo.MongoClient) -> None:
        self.conn = connection
        
    @classmethod
    def connect(cls, uri: str) -> Self:
        """
        Establishes a connection to the MongoDB database.

        Parameters
        ----------
        uri : str
            The MongoDB connection URI.

        Returns
        -------
        MongoClient
            An instance of MongoClient with an active connection.
            
        Raises
        ------
        InterfaceError
            When the client fails to handle a connection failure to the
            database.
        """
        try:
            conn = pymongo.MongoClient(uri)
            return cls(conn)
        except Exception as e:
            raise InterfaceError(e)
        
    def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            self.conn.close()
            self.conn = None
        