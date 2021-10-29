from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Union

from .enums import MatchMode

__all__ = ("LanguageRepresentation", "CityName", "CityZone", "CityCountdown", "City")


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

    @property
    def languages(self) -> List[str]:
        return [self.he, self.en, self.ru, self.ar, self.es]


class CityName(LanguageRepresentation):
    """
    Represents a city name.
    """


class CityZone(LanguageRepresentation):
    """
    Represents a city zone.
    """


@dataclass
class CityCountdown(LanguageRepresentation):
    """
    Represents a city countdown.
    """

    seconds: int

    @classmethod
    def from_seconds(cls, seconds: int) -> CityCountdown:
        countdown_dict = {
            0: {
                "he": "מיידי",
                "en": "Immediately",
                "ru": "Срочно",
                "ar": "فوري",
                "es": "Inmediatamente",
            },
            15: {
                "he": "15 שניות",
                "en": "15 Seconds",
                "ru": "15 секунд",
                "ar": "15 ثانية",
                "es": "15 Segundos",
            },
            30: {
                "he": "30 שניות",
                "en": "30 Seconds",
                "ru": "30 секунд",
                "ar": "30 ثانية",
                "es": "30 Segundos",
            },
            45: {
                "he": "45 שניות",
                "en": "45 Seconds",
                "ru": "45 секунд",
                "ar": "45 ثانية",
                "es": "45 Segundos",
            },
            60: {
                "he": "דקה",
                "en": "One minute",
                "ru": "Минута",
                "ar": "دقيقة",
                "es": "Un minuto",
            },
            90: {
                "he": "דקה וחצי",
                "en": "One and a half minutes",
                "ru": "1.5 минуты",
                "ar": "دقيقة ونصف",
                "es": "Un minuto y medio",
            },
            180: {
                "he": "3 דקות",
                "en": "3 minutes",
                "ru": "3 минуты",
                "ar": "3 دقائق",
                "es": "3 minuto",
            },
        }

        return cls(**countdown_dict.get(seconds), seconds=seconds)


@dataclass
class City:
    """
    Represents city information.
    """

    name: CityName
    zone: CityZone
    countdown: CityCountdown
    lat: float
    lng: float

    @staticmethod
    def _city_name_match(city_name: str, city_data: Dict[str, Any], match_mode: MatchMode) -> bool:
        city_keys = ["he", "en", "ar", "ru", "es"]
        city_names = [name for key, name in city_data.items() if key in city_keys]

        for api_city_name in city_names:
            matches = {
                MatchMode.EXACT: city_name == api_city_name,
                MatchMode.IN: city_name in api_city_name,
            }

            match = matches.get(match_mode)

            if match:
                return True

        return False

    @classmethod
    def from_city_name(
        cls, city_name: str, city_data: List[Dict[str, Any]]
    ) -> Union[City, str]:
        """
        Returns a CityInformation object from a city name.
        The city name can be in hebrew, arabic, english, russian or spanish.

        :param List[Dict[str, Any]] city_data: The city data to get the city from.
        :param str city_name: The city name.
        :return: The city or the city_name (str) if the city cannot be found (old cities).
        :rtype: Union[City, str]
        """

        city_dict = next(
            (
                city for city in city_data if cls._city_name_match(city_name, city, MatchMode.EXACT)
            ),
            None
        )

        if city_dict:
            return cls.from_dict(city_dict)

        priorities = [
            [city for city in city_data if cls._city_name_match(city_name, city, mode)]
            for mode in MatchMode if mode != MatchMode.EXACT
        ]  # Only use priorities if MatchMode.EXACT failed, to save time and memory.

        for priority in priorities:
            city_dict = next(iter(priority), None)

            if city_dict:
                return cls.from_dict(city_dict)

        return city_name  # In case the city name is not in the city list.

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
        zone_dict = values[5]
        countdown_seconds = values[6]

        return cls(
            CityName(*city_values),
            CityZone(*zone_dict.values()),
            CityCountdown.from_seconds(countdown_seconds),
            *values[7:]
        )
