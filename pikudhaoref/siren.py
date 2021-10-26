from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pytz
from typing import Dict, List, Any

from .city import City

__all__ = ("Siren",)


@dataclass
class Siren:
    """
    Represents a siren.
    """

    city: City
    datetime: datetime

    @classmethod
    def from_raw(cls, raw: Dict[str, str], city_data: List[Dict[str, Any]]) -> Siren:
        """
        Returns a Siren object from the dictionary.

        :param List[Dict[str, Any]] city_data: The city data to fetch.
        :param Dict[str, str] raw: The raw dictionary.
        :return: The siren object.
        :rtype: Siren
        """

        israel_timezone = pytz.timezone("Israel")
        date = datetime.strptime(raw["datetime"], "%Y-%m-%dT%H:%M:%S")

        return cls(
            City.from_city_name(raw["data"], city_data),
            israel_timezone.localize(date).astimezone(pytz.utc),
        )
