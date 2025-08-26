
from datetime import datetime
from typing import AsyncGenerator, Protocol

import httpx

from models.activities import ActivityMetadata
from storage import StorageBackend



class StravaAuth(Protocol): ...


class StravaClientSecret(StravaAuth):
    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self._auth_url = "https://www.strava.com/oauth/token"

    def _get_access_token(self):
        payload = {
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "f": "json",
        }

        response = httpx.post(self._auth_url, data=payload, verify=False)
        response.raise_for_status()

        result = response.json()
        return result["access_token"]


class StravaDownloader:
    def __init__(self, auth: StravaAuth, storage: StorageBackend) -> None:
        self.auth = auth
        self.storage = storage

        self._base_url = "https://www.strava.com/api/v3"
        self._download_url = "https://www.strava.com/activities/{activity_id}/export_gpx"

    async def list_activities(self, client: httpx.AsyncClient) -> AsyncGenerator[dict, dict]:
        start_date = datetime(2000, 1, 1).timestamp()

        while start_date < datetime.now():
            response = await client.get(
                f"{self._base_url}/athlete/activities",
                params={"page": 1, "per_page": 100, "after": start_date},
            )
            response.raise_for_status()

            payload = response.json()
            start_date = datetime.fromisoformat(payload[-1]["start_date"]).timestamp()

            yield payload

    def _extract_activity_metadata(self, activity: dict) -> ActivityMetadata:
        return ActivityMetadata(
            id=activity["id"],
            name=activity["name"],
            distance=activity["distance"],
            moving_time=activity["moving_time"],
            elapsed_time=activity["elapsed_time"],
            type=activity["type"],
            start_date=activity["start_date"],
        )

    async def download_gpx_file(self, client: httpx.AsyncClient, activity_id: int) -> bytes:
        response = await client.get(self._download_url.format(activity_id=activity_id))
        response.raise_for_status()

        return response.content

    async def download(self):
        activity_ids = []
        async with self.auth as client:
            for activities in self.list_activities(client):
                for activity in activities:
                    activity_metadata = self._extract_activity_metadata(activity)
                    activity_ids.append(activity_metadata.id)
