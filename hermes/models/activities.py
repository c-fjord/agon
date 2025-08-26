from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from enum import StrEnum, auto


class ActivityType(StrEnum):
    RUNNING = auto()
    CYCLING = auto()
    ELLIPTICAL = auto()


class Sex(StrEnum):
    MALE = auto()
    FEMAL = auto()
    OTHER = auto()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    sex: Mapped[Enum[Sex]]

    def __repr__(self):
        return f"""
            User(
                id={self.id!r},
                username={self.username!r},
                city={self.city!r},
                country={self.city!r},
                sex={self.sex!r})
        """


class ActivityMetadata(Base):
    __tablename__ = "activity_metadata"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    distance: Mapped[float]
    moving_time: Mapped[float]
    elapsed_time: Mapped[float]
    type: Mapped[Enum[ActivityType]]
    start_date: Mapped[datetime]

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


class ActivityDataPoint(Base):
    __tablename__ = "activity_data_point"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int]
    latitude: Mapped[float]
    longitude: Mapped[float]
    elevation: Mapped[float]
    heart_rate: Mapped[Optional[float]]

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self):
        pass
