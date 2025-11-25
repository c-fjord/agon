import polars as pl
from typing import Protocol

from models.activities import ActivityMetadata
from repository.database import DatabaseConnection

# from models.activities import ActivityMetadata, User


class StorageBackend[T](Protocol):
    async def insert(self, entry: T) -> int: ...
    async def update(self, entry: T) -> T: ...
    async def get(self, id: str) -> T: ...
    async def delete(self, id: str) -> T: ...


class ActivityMetadataRepository(StorageBackend[ActivityMetadata]):
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    async def insert(self, entry: ActivityMetadata) -> int:
        if entry.id != 0:
            raise ValueError(
                "Cannot assing id when inserting 'ActivityMetadata' the database will handle id generation"
            )

        entry_id = await self.db.execute(
            """
            INSERT INTO activities (name, moving_time, elapsed_time, type, start_date, distance)
            VALUES (%(name)s, %(moving_time)s, %(elapsed_time)s, %(type)s, %(start_date)s, %(distance)s)
            RETURNING id;
            """,
            entry.model_dump(),
        )

        return entry_id

    async def update(self, entry: ActivityMetadata) -> ActivityMetadata:
        raise NotImplementedError("Has not been implemented!")

    async def get(self, id: str) -> ActivityMetadata:
        activity = await self.db.execute(
            """
            SELECT id, name, moving_time, elapsed_time, type, start_date, distance 
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
        activity = await self.db.execute(
            """
            DELETE FROM activities 
            WHERE id = %s id
            RETURNING name, moving_time, elapsed_time, type, start_date, distance 
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


class ActivityDataRepository(StorageBackend[pl.DataFrame]):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    async def insert(self, entry: pl.DataFrame) -> int:
        self.db.execute_many(
            """
            INSERT INTO activity_data (time, latitude, longitude, altitude, heartrate, distance, activity_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            entry.select(
                pl.col(["time", "latitude", "longitude", "altitude", "heartrate", "distance", "activity_id"])
            ).rows(),
        )

    async def update(self, entry: pl.DataFrame) -> pl.DataFrame:
        raise NotImplementedError("Has not been implemented")

    async def get(self, id: str) -> pl.DataFrame:
        raise NotImplementedError("Has not been implemented!")

    async def delete(self, id: str) -> pl.DataFrame:
        self.db.execute("DELETE FROM WHERE id", (id,))
