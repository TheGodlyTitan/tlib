import unittest

import asyncio
from typing import TypeAlias, Union

from database import (
    SqliteClient,
    PostgreClient,
    MongoClient,
    AsyncSqliteClient,
    AsyncPostgreClient,
    AsyncMongoClient
)
from database.errors import (
    ConnectionError
)


ClientType: TypeAlias = Union[
    SqliteClient,
    PostgreClient,
    MongoClient,
    AsyncSqliteClient,
    AsyncPostgreClient,
    AsyncMongoClient,
]


class TestConnections(unittest.TestCase):
    
    def setUp(self):
        # Correct Connections
        self.sqlite_file = 'tlib_tests/database_tests/databases/tests.db'
        self.sqlite_wrong_file = 'tlib_tests/database_tests/databases/tests.txt'
        
        self.postgre_credentials = {
            "database": "tlib_test",
            "user": "postgres",
            "password": "tlib_pass",
            "host": "localhost",
            "port": 5432,
        }
        self.postgre_dsn = "postgresql://postgres:tlib_pass@localhost:5432/tlib_test"
        self.postgres_wrong_db = "postgresql://postgres:tlib_pass@localhost:5432/NODATABASE" # Invalid database: 'NODATABASE'
        self.postgres_wrong_user = "postgresql://NOUSER:tlib_pass@localhost:5432/tlib_test" # Invalid user: 'NOUSER'
        self.postgres_wrong_host = "postgresql://postgres:tlib_pass@NOHOST:5432/tlib_test" # Invalid host: 'NOHOST' 
        self.postgres_wrong_port = "postgresql://postgres:tlib_pass@localhost:1111/tlib_test" # Invalid port: "1111"
        self.postgres_invalid_port = "postgresql://postgres:tlib_pass@localhost:NOPORT/tlib_test" # Invalid port: "NOPORT"
        
        self.mongo_uri = "mongodb+srv://tlib_user:tlib_pw@cluster0.u4thvsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        self.mongo_wrong_pass = "mongodb+srv://tlib_user:wrong_pw@cluster0.u4thvsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_wrong_user = "mongodb+srv://wrong_user:tlib_pw@cluster0.u4thvsm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_wrong_cluster = "mongodb+srv://tlib_user:tlib_pw@wrongcluster.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_invalid_uri = "mongodb://invalid-uri"
        
    """Test Helpers"""

    def assertConnected(self, db: ClientType) -> None:
        self.assertTrue(db.is_connected())
    
    def assertDisconnected(self, db: ClientType) -> None:
        self.assertFalse(db.is_connected())
        
    def assertSynchronous(self, db: ClientType) -> None:
        self.assertFalse(db.is_async())
    
    def assertAsynchronous(self, db: ClientType) -> None:
        self.assertTrue(db.is_async())
    
    """Synchronous Connections"""
    
    def test_sync_sqlite(self) -> None:
        db = SqliteClient.connect(self.sqlite_file)
        self.assertSynchronous(db)
        self.assertConnected(db)
        db.close()
        self.assertDisconnected(db)
    
    def test_sync_postgre_credentials(self) -> None:
        db = PostgreClient.connect(**self.postgre_credentials)
        self.assertSynchronous(db)
        self.assertConnected(db)
        db.close()
        self.assertDisconnected(db)
        
    def test_sync_postgre_dsn(self) -> None:
        db = PostgreClient.connect(dsn=self.postgre_dsn)
        self.assertSynchronous(db)
        self.assertConnected(db)
        db.close()
        self.assertDisconnected(db)
        
    def test_sync_mongo_uri(self) -> None:
        db = MongoClient.connect(uri=self.mongo_uri)
        self.assertSynchronous(db)
        self.assertConnected(db)
        db.close()
        self.assertDisconnected(db)
        
    """Asynchronous Connections"""
    
    def test_async_sqlite(self) -> None:
        async def test():
            db = await AsyncSqliteClient.connect(self.sqlite_file)
            self.assertAsynchronous(db)
            self.assertConnected(db)
            await db.close()
            self.assertDisconnected(db)
        asyncio.run(test())
         
    def test_async_postgre_credentials(self) -> None:
        async def test():
            db = await AsyncPostgreClient.connect(**self.postgre_credentials)
            self.assertAsynchronous(db)
            self.assertConnected(db)
            await db.close()
            self.assertDisconnected(db)
        asyncio.run(test())
            
    def test_async_postgre_dsn(self) -> None:
        async def test():
            db = await AsyncPostgreClient.connect(dsn=self.postgre_dsn)
            self.assertAsynchronous(db)
            self.assertConnected(db)
            await db.close()
            self.assertDisconnected(db)
        asyncio.run(test())
    
    def test_async_mongo_uri(self) -> None:
        async def test():
            db = await AsyncMongoClient.connect(uri=self.mongo_uri)
            self.assertAsynchronous(db)
            self.assertConnected(db)
            await db.close()
            self.assertDisconnected(db)
        asyncio.run(test())
            
    """Failed Connections"""
    
    def test_sync_sqlite_wrong_file(self) -> None:
        with self.assertRaises(ConnectionError):
            SqliteClient.connect(self.sqlite_wrong_file)
    
    def test_async_sqlite_wrong_file(self) -> None:
        async def test():
            await AsyncSqliteClient.connect(self.sqlite_wrong_file)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
    
        
    def test_sync_postgre_wrong_db(self) -> None:
        with self.assertRaises(ConnectionError):
            PostgreClient.connect(dsn=self.postgres_wrong_db)
    
    def test_sync_postgre_wrong_user(self) -> None:
        with self.assertRaises(ConnectionError):
            PostgreClient.connect(dsn=self.postgres_wrong_user)
    
    def test_sync_postgre_wrong_host(self) -> None:
        with self.assertRaises(ConnectionError):
            PostgreClient.connect(dsn=self.postgres_wrong_host)
    
    def test_sync_postgre_wrong_port(self) -> None:
        with self.assertRaises(ConnectionError):
            PostgreClient.connect(dsn=self.postgres_wrong_port)
            
    def test_sync_postgre_invalid_port(self) -> None:
        with self.assertRaises(ConnectionError):
            PostgreClient.connect(dsn=self.postgres_invalid_port)
            
    
    def test_async_postgre_wrong_db(self) -> None:
        async def test():
            await AsyncPostgreClient.connect(dsn=self.postgres_wrong_db)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
        
    def test_async_postgre_wrong_user(self) -> None:
        async def test():
            await AsyncPostgreClient.connect(dsn=self.postgres_wrong_user)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
    
    def test_async_postgre_wrong_host(self) -> None:
        async def test():
            await AsyncPostgreClient.connect(dsn=self.postgres_wrong_host)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
    
    def test_async_postgre_wrong_port(self) -> None:
        async def test():
            await AsyncPostgreClient.connect(dsn=self.postgres_wrong_port)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
            
    def test_async_postgre_invalid_port(self) -> None:
        async def test():
            await AsyncPostgreClient.connect(dsn=self.postgres_invalid_port)
        with self.assertRaises(ConnectionError):
            asyncio.run(test())
            
            


        