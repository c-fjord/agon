from datetime import datetime, time
from typing import Optional
from enum import StrEnum, auto

from pydantic import BaseModel, Field



class ActivityType(StrEnum):
    RUNNING = auto()
    CYCLING = auto()
    ELLIPTICAL = auto()
    WORKOUT = auto()

def strava_activity_type(activity_type: str) -> ActivityType:
    match activity_type.lower():
        case "elliptical":
            return ActivityType.ELLIPTICAL
        case "ride":
            return ActivityType.CYCLING
        case "run":
            return ActivityType.RUNNING
        case "virtualride":
            return ActivityType.CYCLING
        case "virtualrun":
            return ActivityType.RUNNING
        case "workout":
            return ActivityType.WORKOUT

class Sex(StrEnum):
    MALE = auto()
    FEMAL = auto()
    OTHER = auto()



class User(BaseModel):
    id: str
    username: str
    city: str
    country: str
    sex: Sex

    def __repr__(self):
        return f"""
            User(
                id={self.id!r},
                username={self.username!r},
                city={self.city!r},
                country={self.city!r},
                sex={self.sex!r})
        """


class ActivityMetadata(BaseModel):
    id: int = Field(default=0)
    name: str
    distance: float
    moving_time: time
    elapsed_time: time
    type: ActivityType
    start_date: datetime

    def __repr__(self) -> str:
        return f"""
            Activity(
                id={self.id!r},
                name={self.name!r},
                distance={self.distance!r},
                moving_time={self.moving_time!r},
                elapsed_time={self.elapsed_time!r},
                type={self.type!r},
                start_date={self.start_date!r})
        """