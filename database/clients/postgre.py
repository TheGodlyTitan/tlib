import re
from typing_extensions import Self

import psycopg2

from database import Client
from database.errors import (
    ConnectionError,
    InterfaceError,
)


def extract_psycopg2_connection_error(error: psycopg2.OperationalError) -> str:
    """
    Extracts the relevant failure reason from a PostgreSQL connection error.

    Parameters
    ----------
    error : psycopg2.OperationalError
        The exception raised when attempting a connection.

    Returns
    -------
    str
        A cleaned-up error message with only the failure reason.
    """
    error_message = str(error)

    # Check for "FATAL:" and extract the specific reason
    match = re.search(r"FATAL:\s*(.*)", error_message)
    if match:
        return match.group(1)

    # Handle host-related errors
    if "could not translate host name" in error_message:
        return 'Unknown Host'
    
    if 'Is the server running on that host and accepting TCP/IP connections?' in error_message:
        return 'Connection Refused'

    # Handle general connection errors
    return error_message  # Fallback to the full message if no pattern matches
    
    
class PostgreClient(Client):
    """
    Synchronous PostgreSQL database client implementation
    Uses `psycopg2` for synchronous database interactions. 
    """
    
    def __init__(self, connection: psycopg2.extensions.connection):
        self.conn = connection
    
    @classmethod
    def connect(
        cls,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = "localhost",
        port: int = 5432,
        dsn: str = None,
    ) -> Self:
        """
        Establishes a synchronous connection to the PostgreSQL database.

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
        PostgresClient
            An instance of PostgreClient with an active database connection.
            
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
            
            if dsn:
                conn = psycopg2.connect(dsn)
            else:
                conn = psycopg2.connect(
                    database=database,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                )
            return cls(conn)
        
        except psycopg2.OperationalError as e:
            msg = extract_psycopg2_connection_error(e)
            raise ConnectionError(msg)
        
        except Exception as e:
            raise InterfaceError(e)
    
    def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            self.conn.close()
            self.conn = None
