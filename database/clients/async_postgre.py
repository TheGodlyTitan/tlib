from typing_extensions import Self

import asyncpg
from asyncpg import exceptions
import socket

from database import Client
from database.errors import (
    ConnectionError,
    InterfaceError
)


class AsyncPostgreClient(Client):
    """
    Asynchronous PostgresSQL database client implementation
    Uses `asyncpg` for asynchronous database interactions.
    """

    def __init__(self, connection: asyncpg.Connection):
        self.conn = connection
        
    @classmethod
    async def connect(
        cls,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = "localhost",
        port: int = 5432,
        dsn: str = None,
    ) -> Self:
        """
        Establishes an asynchronous connection to the PostgreSQL database.

        Parameters
        ----------
        database : str, optional
            The name of the database to connect to.
        user : str, optional
            The username for authentication.
        password : str, optional
            The password for authentication.
        host : str, optional
            The database server host. Defaults to "localhost".
        port : int, optional
            The port to connect on. Defaults to 5432.
        dsn : str, optional
            The PostgreSQL DSN (Data Source Name) or connection string.
            If provided, it overrides other parameters.

        Returns
        -------
        AsyncPostgreClient
            An instance of AsyncPostgreClient with an active database connection.
            
        Raises
        ------
        ConnectionError
            When the client fails to connect to the database. Likely from
            incorrect database credentials.
        InterfaceError
            When the client fails to handle a connection failure to the
            database.
        """
        try:
            # Check if DSN is provided, if not, validate the required fields
            if dsn:
                conn = await asyncpg.connect(dsn)
            else:
                # Attempt to connect using the provided credentials and parameters
                conn = await asyncpg.connect(
                    database=database,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                )

            return cls(conn)
        
        except exceptions.InvalidCatalogNameError as e:
            raise ConnectionError(e)
        
        except exceptions.InvalidAuthorizationSpecificationError as e:
            raise ConnectionError(e)
        
        except socket.gaierror as e:
            raise ConnectionError('Unknown host')
        
        except ConnectionRefusedError as e:
            raise ConnectionError('Connection Refused')
        
        except ValueError as e:
            raise ConnectionError(e)
        
        except Exception as e:
            raise InterfaceError(e)
            
    
    async def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            await self.conn.close()
            self.conn = None
