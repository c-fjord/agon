from psycopg.connection_async import AsyncConnection
import polars as pl
from typing import Protocol

from models.activities import ActivityMetadata, User


class StorageBackend(Protocol): ...


class TimescaleDB(StorageBackend):
    _conn = None

    def __init__(self, conn_str: str) -> None:
        self._conn_str = conn_str

    async def start(self) -> None:
        self._conn = await AsyncConnection.connect(self._conn_str)

    async def insert_activity(self, activity_data_points: pl.DataFrame) -> None:
        async with await AsyncConnection.connect(self.conn_str) as conn:
            async with conn.cursor() as cur:
                await cur.execute()

    async def get_activity(self, activity_id: int) -> pl.DataFrame:
        async with await AsyncConnection.connect(self.conn_str) as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM X WHERE activity_id=%s", (activity_id,))

    async def insert_user(self, user: User) -> None:
        pass

    async def get_user(self, user_id: int) -> User:
        pass

    async def insert_activity_metadata(self, metadata: ActivityMetadata) -> None:
        pass

    async def get_activity_metadata(self, metadata_id: int) -> ActivityMetadata:
        pass
