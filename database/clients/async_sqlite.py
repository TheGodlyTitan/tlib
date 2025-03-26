import os
from typing import Union, Any
from typing_extensions import Self

import aiosqlite

from database import Client
from database.errors import (
    ConnectionError,
    InterfaceError
)


class AsyncSqliteClient(Client):
    """
    Asynchronous Sqlite database client implementation
    Uses `aiosqlite` for asynchronous database interactions.
    """

    def __init__(self, connection: aiosqlite.Connection):
        self.conn = connection

    @classmethod
    async def connect(cls, db_path: os.PathLike) -> Self:
        """
        Establishes a connection to the SQLite database.

        Parameters
        ----------
        db_path : os.PathLike
            The path to the SQLite database file.

        Returns
        -------
        AsyncSqliteClient
            An instance of AsyncSqliteClient with an active connection.
        
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
            conn = await aiosqlite.connect(db_path)
            return cls(conn)
        
        except Exception as e:
            raise InterfaceError(e)

    async def close(self) -> None:
        """Closes the connection to the database."""
        if self.is_connected():
            await self.conn.close()
            self.conn = None
        
    async def execute(
        self, 
        query: str, 
        params: Union[tuple, list] = (),
        commit: bool = True
    ) -> Union[int, Any]:
        """
        Executes a query on the SQLite database asynchronously.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        params : Optional[`list`, `tuple`]
            The parameters to pass into the SQL query, defaults to an empty tuple.
        commit : Optional[`bool`]
            Whether to commit the transaction for non-SELECT queries, defaults to True.
            
        Returns
        -------
        Union[int, Any]
            For SELECT queries, returns the rows fetched. 
            For other queries, returns the number of affected rows.
        
        Raises
        ------
        Exception
            If the query execution fails.
        """
        if not self.is_connected():
            raise Exception("No active connection to the database.")

        async with self.conn.cursor() as cursor:
            try:
                # Execute the query with parameters
                await cursor.execute(query, params)

                # If it's a SELECT query, fetch the results
                if query.strip().lower().startswith("select"):
                    return await cursor.fetchall()  # Return all rows
                else:
                    # Commit for non-SELECT queries
                    if commit:
                        await self.conn.commit()
                    # Return number of affected rows
                    return cursor.rowcount  

            except Exception as e:
                raise Exception(f"Error executing query: {str(e)}")
            