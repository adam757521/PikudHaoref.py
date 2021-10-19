from __future__ import annotations

from datetime import datetime

import pytz
from typing import Dict

from .city import City

__all__ = ("Siren",)


class Siren:
    """
    Represents a siren.
    """

    __slots__ = ("city", "datetime")

    def __init__(self, city: City, datetime_: datetime):
        self.datetime = datetime_
        self.city = city

    def __str__(self):
        return f"<{self.__class__.__name__} city={self.city}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} city={self.city}, datetime={self.datetime}>"

    @classmethod
    def from_raw(cls, raw: Dict[str, str]) -> Siren:
        """
        Returns a Siren object from the dictionary.

        :param Dict[str, str] raw: The raw dictionary.
        :return: The siren object.
        :rtype: Siren
        """

        israel_timezone = pytz.timezone("Israel")
        date = datetime.strptime(raw["alertDate"], "%Y-%m-%d %H:%M:%S")

        return cls(
            City.from_city_name(raw["data"]),
            israel_timezone.localize(date).astimezone(pytz.utc),
        )
