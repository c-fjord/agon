import polars as pl
import io
from gpxcsv import gpxtolist


from typing import Protocol

class Parser(Protocol):
    def parse(self, data: bytes) -> pl.DataFrame: ...

class GPXParser:
    def parse(self, data: bytes) -> pl.DataFrame:
        df = pl.from_dict(gpxtolist(io.StringIO(data.decode("UTF-8"))))
        return df

# df[["lat_start", "lon_start", "time_delta"]] = df[["lat", "lon", "time"]].shift(1)
# df["time_delta"] = df.apply(lambda row: (row["time"] - row["time_delta"]).seconds, axis=1)
# df["distance"] = df.apply(
#     lambda row: calculate_distance(row["lat_start"], row["lat"], row["lon_start"], row["lon"]), axis=1)
# df["pace"] = df.apply(lambda row: calculate_pace(row["time_delta"], row["distance"]), axis=1)