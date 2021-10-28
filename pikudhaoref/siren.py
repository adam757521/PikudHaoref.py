from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pytz
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .city import City

__all__ = ("Siren",)


@dataclass
class Siren:
    """
    Represents a siren.
    """

    city: City | str
    datetime: datetime

    @classmethod
    def from_raw(cls, raw: Dict[str, str]) -> Siren:
        """
        Returns a Siren object from the dictionary.

        :param Dict[str, str] raw: The raw dictionary.
        :return: The siren object.
        :rtype: Siren
        """

        israel_timezone = pytz.timezone("Israel")
        date = datetime.strptime(raw["datetime"], "%Y-%m-%dT%H:%M:%S")

        return cls(
            raw["data"], israel_timezone.localize(date).astimezone(pytz.utc),
        )
