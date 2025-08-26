from dotenv import load_dotenv
import os

from hermes.downloader.strava import StravaDownloader, StravaClientSecret
from hermes.storage import TimescaleDB

if __name__ == "__main__":
    load_dotenv()

    client_secret = StravaClientSecret(
                        client_id=os.getenv("CLIENT_ID"), 
                        client_secret=os.getenv("CLIENT_SECRET"),
                        refresh_token=os.getenv("REFRESH_TOKEN")
                    )

    storage = TimescaleDB(os.getenv("CONNECTION_STRING"))
    downloader = StravaDownloader(auth=client_secret, storage=storage)

    downloader.list_activities()

