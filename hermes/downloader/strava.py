
from datetime import datetime
import json
from typing import AsyncGenerator

import httpx

from models.activities import ActivityMetadata
import polars as pl

from models.activities import strava_activity_type


class StravaAuth(httpx.Auth):
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        
        self._access_token: str | None = None
        self._refresh_url = "https://www.strava.com/oauth/token"

    def _build_refresh_request(self) -> httpx.Request:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "f": "json",
        }
        return httpx.Request("POST", self._refresh_url, json=payload)

    def _update_token(self, response: httpx.Response) -> None:
        payload = json.loads(response.read())
        self._access_token = f"Bearer {payload['access_token']}"

    def sync_auth_flow(self, request: httpx.Request):
        if self._access_token is not None:
            request.headers["Authorization"] = self._access_token
            response: httpx.Response = yield request

        if self._access_token is None or response.status_code == 401:
            refresh_response = yield self._build_refresh_request()
            self._update_token(refresh_response)

            request.headers["Authorization"] = self._access_token
            yield request

    async def _async_update_token(self, response: httpx.Response) -> None:
        payload = await response.aread()
        data = json.loads(payload)
        self._access_token = f"Bearer {data['access_token']}"

    async def async_auth_flow(self, request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        if self._access_token is not None:
            request.headers["Authorization"] = self._access_token
            response: httpx.Response = yield request

        if self._access_token is None or response.status_code == 401:
            refresh_response = yield self._build_refresh_request()
            await self._async_update_token(refresh_response)

            request.headers["Authorization"] = self._access_token
            yield request

class StravaDownloader:
    def __init__(self, auth: StravaAuth) -> None:
        self.auth = auth
        self._base_url = "https://www.strava.com/api/v3"
        
    async def list_activities(self, client: httpx.AsyncClient, last_end_date: datetime | None = None) -> AsyncGenerator:
        if last_end_date is None:
            start_date = datetime(2000, 1, 1).timestamp()
        else: 
            start_date = last_end_date.timestamp()

        while start_date < datetime.now().timestamp():
            response = await client.get(
                f"{self._base_url}/athlete/activities",
                params={"page": 1, "per_page": 5, "after": start_date},
            )
            response.raise_for_status()

            activities = response.json()

            if len(activities) > 0:
                start_date = datetime.fromisoformat(activities[-1]["start_date"]).timestamp()

                for activity in activities:
                    yield activity

    def _extract_activity_metadata(self, activity: dict) -> ActivityMetadata:
        return ActivityMetadata(
            id=activity["id"],
            name=activity["name"],
            distance=activity["distance"],
            moving_time=activity["moving_time"],
            elapsed_time=activity["elapsed_time"],
            type=strava_activity_type(activity["type"]),
            start_date=activity["start_date"],
        )

    # TODO: Anonymous downloads of GPX files of publich activities is not longer supported. 
    # Needs to be logging in. 
    # async def _download_gpx_file(self, client: httpx.AsyncClient, activity_id: int) -> bytes | None:
    #     response = await client.get(self._download_url.format(activity_id=activity_id))
    #     response.raise_for_status()            
    #     return response.content

    async def _download_streams(self, client: httpx.AsyncClient, activity_id: str) -> pl.DataFrame:
        response = await client.get(
            url=f"{self._base_url}/activities/{activity_id}/streams?keys=time,distance,latlng,altitude,heartrate&key_by_type=true")
        
        response.raise_for_status()
        payload = response.json()

        data = {}
        for key in ["time", "latlng", "altitude", "distance", "heartrate"]:
            if key in payload:
                data[key] = payload[key]["data"]

        df = pl.from_dict(data)

        if "latlng" in payload:
            df = df.with_columns([
                pl.col("latlng").list.get(0).alias("latitude"),
                pl.col("latlng").list.get(1).alias("longitude")
            ]).drop("latlng")

        return df

    async def download(self, last_end_date: datetime | None = None):
        async with httpx.AsyncClient(auth=self.auth) as client:
            async for activity in self.list_activities(client, last_end_date):
                activity_metadata = self._extract_activity_metadata(activity)
                streams = await self._download_streams(client, activity["id"])
                yield activity_metadata, streams

    