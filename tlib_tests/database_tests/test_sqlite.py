import unittest
import asyncio

from database import (
    SqliteClient,
    AsyncSqliteClient
)




class TestSqlite(unittest.TestCase):
    
    def setUp(self):
        self.sqlite_file = 'tlib_tests/database_tests/databases/tests.db'
        
    """SqliteClient Tests"""
    # TODO
    
    """AsyncSqliteClient Tests"""
    
    def test_async_create_table(self) -> None:
        async def test():
            db = await AsyncSqliteClient.connect(self.sqlite_file)
            query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
            """
            await db.execute(query)
            await db.close()
        asyncio.run(test())
    
    def test_async_insert(self) -> None:
        async def test():
            db = await AsyncSqliteClient.connect(self.sqlite_file)
            await db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 10))
            await db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 10))
            await db.close()
        asyncio.run(test())
        
    def test_async_update(self) -> None:
        async def test():
            db = await AsyncSqliteClient.connect(self.sqlite_file)
            await db.execute("UPDATE users SET age = ? WHERE name = ?", (15, 'Alice'))
            await db.execute("UPDATE users SET age = ? WHERE name = ?", (15, 'Bob'), commit=False)
            await db.close()
        asyncio.run(test())
        
    def test_async_fetch(self) -> None:
        async def test():
            db = await AsyncSqliteClient.connect(self.sqlite_file)
            await db.execute("SELECT * WHERE name = ?", ('Alice'))
        
            
        