import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

from downloader.strava import StravaDownloader, StravaAuth
from repository.storage import TimescaleDB


async def main():
    client_secret = StravaAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        refresh_token=os.getenv("REFRESH_TOKEN"),
    )

    downloader = StravaDownloader(auth=client_secret)
    storage = TimescaleDB(os.getenv("CONNECTION_STRING"))

    async for metadata, data in downloader.download(datetime(2025, 5, 1)):
        print(metadata, data)


if __name__ == "__main__":
    load_dotenv()

    asyncio.run(main())
