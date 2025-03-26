import os
from typing_extensions import Self

import sqlite3

from database import Client
from database.errors import (
    ConnectionError,
    InterfaceError,
)


class SqliteClient(Client):
    """
    Synchronous Sqlite database client implementation
    Uses `sqlite3` for synchronous database interactions.
    """

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    @classmethod
    def connect(cls, db_path: os.PathLike) -> Self:
        """
        Establishes a connection to the SQLite database.

        Parameters
        ----------
        db_path : os.PathLike
            The path to the SQLite database file.

        Returns
        -------
        SqliteClient
            An instance of SqliteClient with an active connection.
        
        Raises
        ------
        ConnectionError
            When the provided db_path does not have a `.db` extension.
        InterfaceError
            When the client fails to handle a connection failure to the
            database.
        """
        # Check if the provided db_path ends with '.db'
        if not str(db_path).endswith('.db'):
            raise ConnectionError("The database path must end with a '.db' file extension.")
        
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(db_path)
            return cls(conn)
        
        except Exception as e:
            raise InterfaceError(e)

    def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            self.conn.close()
            self.conn = None


