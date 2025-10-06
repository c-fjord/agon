import polars as pl
from typing import Protocol

from hermes.models.activities import ActivityMetadata
from repository.database import PostgresDBConnection

# from models.activities import ActivityMetadata, User


class StorageBackend[T](Protocol):
    async def insert(self, entry: T) -> int: ...
    async def update(self, entry: T) -> T: ...
    async def get(self, id: str) -> T: ...
    async def delete(self, id: str) -> T: ...


class ActivityMetadataRepository(StorageBackend[ActivityMetadata], PostgresDBConnection):
    def __init__(self, conn_str: str) -> None:
        super().__init__(conn_str)

    async def insert(self, entry: ActivityMetadata) -> int:
        if entry.id != 0:
            raise ValueError(
                "Cannot assing id when inserting 'ActivityMetadata' the database will handle id generation"
            )

        entry_id = await self.execute(
            """
            INSERT INTO activities (name, moving_time, elapsed_time, activity_type, start_date, distance)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (entry.name, entry.moving_time, entry.elapsed_time, entry.type, entry.start_date, entry.distance),
        )

        return entry_id

    async def update(self, entry: ActivityMetadata) -> ActivityMetadata:
        raise NotImplementedError("Has not been implemented!")

    async def get(self, id: str) -> ActivityMetadata:
        activity = await self.execute(
            """
            SELECT id, name, moving_time, elapsed_time, activity_type, start_date, distance 
            FROM activities WHERE id = %s;
            """,
            (id,),
        )

        return ActivityMetadata(
            id=activity[0],
            name=activity[1],
            moving_time=activity[2],
            elapsed_time=activity[3],
            type=activity[4],
            start_date=activity[5],
            distance=activity[6],
        )

    async def delete(self, id: str) -> ActivityMetadata:
        activity = await self.execute(
            """
            DELETE FROM activities 
            WHERE id = %s id
            RETURNING name, moving_time, elapsed_time, activity_type, start_date, distance 
            """,
            (id,),
        )

        return ActivityMetadata(
            id=activity[0],
            name=activity[1],
            moving_time=activity[2],
            elapsed_time=activity[3],
            type=activity[4],
            start_date=activity[5],
            distance=activity[6],
        )


class ActivityDataRepository(StorageBackend[pl.DataFrame], PostgresDBConnection):
    def __init__(self, conn_str):
        super().__init__(conn_str)

    async def insert(self, entry: pl.DataFrame) -> None:
        self.execute_many(
            """
            INSERT INTO activity_data (time, latitude, longitude, altitude, heartrate, distance, activity_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            entry.select(
                pl.col(["time", "latitude", "longitude", "altitude", "heartrate", "distance", "activity_id"])
            ).rows(),
        )

    async def update(self, entry: pl.DataFrame) -> pl.DataFrame:
        raise NotImplementedError("Has not been implemented!")

    async def get(self, id: str) -> pl.DataFrame:
        raise NotImplementedError("Has not been implemented!")

    async def delete(self, id: str) -> pl.DataFrame:
        self.execute("DELETE FROM WHERE id", (id,))
