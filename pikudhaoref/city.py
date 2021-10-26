from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional, List

__all__ = ("LanguageRepresentation", "CityName", "CityZone", "City")


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
    es: str

    def __str__(self):
        return self.en


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
    countdown: int
    lat: float
    lng: float

    @classmethod
    def from_city_name(cls, city_name: str, city_data: List[Dict[str, Any]]) -> Optional[City]:
        """
        Returns a CityInformation object from a city name.
        The city name can be in hebrew, arabic, english, russian or spanish.

        :param List[Dict[str, Any]] city_data: The city data to get the city from.
        :param str city_name: The city name.
        :return: The city if applicable.
        :rtype: Optional[City]
        """

        city_keys = ["he", "en", "ar", "ru", "es"]
        city_dict = next(
            iter(
                [
                    x
                    for x in city_data
                    if city_name.lower()
                    in [name.lower() for key, name in x.items() if key in city_keys]
                ]
            ),
            None,
        )

        if city_dict:
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
        city_values = values[:5]

        return cls(CityName(*city_values), CityZone(*values[5].values()), *values[6:])
