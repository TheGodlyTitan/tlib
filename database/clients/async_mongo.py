from typing_extensions import Self

from motor import motor_asyncio

from database import Client
from database.errors import InterfaceError


class AsyncMongoClient(Client):
    """
    Synchronous MongoDB database client implementation
    Uses `motor` for synchronous database interactions. 
    """
    
    def __init__(self, connection: motor_asyncio.AsyncIOMotorClient):
        self.conn = connection
        
    @classmethod
    async def connect(cls, uri: str) -> Self:
        """
        Establishes an asynchronous connection to the MongoDB database.

        Parameters
        ----------
        uri : str
            The MongoDB connection URI.

        Returns
        -------
        AsyncMongoClient
            An instance of AsyncMongoClient with an active connection.
        
        Raises
        ------
        InterfaceError
            When the client fails to handle a connection failure to the
            database.
        """
        try:
            conn = motor_asyncio.AsyncIOMotorClient(uri)
            return cls(conn)
        
        except Exception as e:
            raise InterfaceError(e)

    async def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            self.conn.close()
            self.conn = None
        
    