from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Union

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

        city_keys = ["he", "en", "ar", "ru", "es"]
        city_dict = next(
            iter(
                [
                    x
                    for x in city_data
                    if any(
                        city_name.lower() in name.lower()
                        for key, name in x.items()
                        if key in city_keys
                    )
                    # Uses this logic because pikudhaoref has changed city identifiers multiple times.
                    # A lot of old cities will not be detected.
                ]
            ),
            None,
        )

        if city_dict:
            return cls.from_dict(city_dict)
        else:
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
