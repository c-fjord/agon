from psycopg.connection_async import AsyncConnection
import polars as pl
from typing import Protocol

from hermes.models.activities import ActivityMetadata

# from models.activities import ActivityMetadata, User


class StorageBackend(Protocol): ...


# create sensor data hypertable
query_create_sensordata_table = """CREATE TABLE sensor_data (
                                        time TIMESTAMPTZ NOT NULL,
                                        sensor_id INTEGER,
                                        temperature DOUBLE PRECISION,
                                        cpu DOUBLE PRECISION,
                                        FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                    );
                                    """

query_create_sensordata_hypertable = "SELECT create_hypertable('sensor_data', by_range('time'));"

class TimescaleDB(StorageBackend):
    _conn = None

    def __init__(self, conn_str: str) -> None:
        self._conn_str = conn_str

    async def start(self) -> None:
        self._conn = await AsyncConnection.connect(self._conn_str)
        async with self._conn.cursor() as cur:
            await cur.execute("")


    async def insert_activity(self, activity_data_points: pl.DataFrame) -> None:
        # https://docs.tigerdata.com/getting-started/latest/start-coding-with-timescale/#create-a-hypertable
        
        async with self._conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO sensors (type, location) VALUES (%s, %s);",
                            (sensor[0], sensor[1]))
            except (Exception, psycopg2.Error) as error:
                print(error.pgerror)
            conn.commit()

        async with await AsyncConnection.connect(self._conn_str) as conn:
            async with conn.cursor() as cur:
                await cur.execute()

    async def get_activity(self, activity_id: int) -> pl.DataFrame:
        async with await AsyncConnection.connect(self._conn_str) as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM X WHERE activity_id=%s", (activity_id,))


    async def insert_activity_metadata(self, metadata: ActivityMetadata) -> None:
        pass

    async def get_activity_metadata(self, metadata_id: int) -> ActivityMetadata:
        pass
