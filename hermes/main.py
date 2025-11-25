import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

import polars as pl
from downloader.strava import StravaDownloader, StravaAuth
from repository.database import PostgresDBConnection
from repository.storage import ActivityDataRepository, ActivityMetadataRepository


async def main():
    client_secret = StravaAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        refresh_token=os.getenv("REFRESH_TOKEN"),
    )

    downloader = StravaDownloader(auth=client_secret)

    postgres_db = PostgresDBConnection(os.getenv("TIMESCALE_CONN_STR"))

    activity_repo = ActivityDataRepository(postgres_db)
    metadata_repo = ActivityMetadataRepository(postgres_db)

    async for metadata, df in downloader.download(datetime(2025, 5, 1)):
        entry_id, *_ = await metadata_repo.insert(metadata)
        df = df.with_columns(pl.lit(entry_id).alias("activity_id"))
        await activity_repo.insert(df)


if __name__ == "__main__":
    load_dotenv()

    asyncio.run(main())
