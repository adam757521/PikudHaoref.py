from __future__ import annotations

import json
from dataclasses import dataclass
import importlib.resources
from typing import Dict, Any, Optional

__all__ = ("LanguageRepresentation", "CityName", "CityZone", "City", "CITY_DATA")

with importlib.resources.open_text("pikudhaoref", "cities.json") as f:
    CITY_DATA = json.load(f)


@dataclass
class LanguageRepresentation:
    """
    Represents a class which adds language representations and language attributes to another class.
    Meant to be inherited.
    """

    he: str
    en: str
    ru: str
    ar: str

    def __str__(self):
        return self.en

    def __repr__(self):
        return f"<{self.__class__.__name__}, he={self.he}, en={self.en}, ru={self.ru}, ar={self.ar}>"


class CityName(LanguageRepresentation):
    """
    Represents a city name.
    """


class CityZone(LanguageRepresentation):
    """
    Represents a city zone.
    """


@dataclass
class City:
    """
    Represents city information.
    """

    name: CityName
    zone: CityZone
    time: int
    lat: float
    lng: float

    @classmethod
    def from_city_name(cls, city_name: str) -> Optional[City]:
        """
        Returns a CityInformation object from a city name.
        The city name can be in hebrew, arabic, english or russian.

        :param str city_name: The city name.
        :return: The city if applicable.
        :rtype: Optional[City]
        """

        city_keys = ["name", "name_en", "name_ar", "name_ru"]
        city_dict = next(
            iter(
                [
                    x
                    for x in CITY_DATA
                    if city_name.lower()
                    in [name.lower() for key, name in x.items() if key in city_keys]
                ]
            ),
            None,
        )

        if not city_dict:
            return

        return cls.from_dict(city_dict)

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> City:
        """
        Returns a CityInformation from the dictionary.

        :param Dict[str, Any] dictionary: The dictionary.
        :return: The city.
        :rtype: City
        """

        values = [
            value for key, value in dictionary.items() if not key.startswith("__")
        ]
        city_values = values[:4]
        zone_values = values[4:8]

        return cls(CityName(*city_values), CityZone(*zone_values), *values[8:])
