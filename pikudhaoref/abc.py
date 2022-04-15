from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Dict
import json

from .city import City
from .base import EventManager
from .exceptions import AccessDenied

if TYPE_CHECKING:
    from datetime import datetime

__all__ = ("HTTPClient", "Client")


class HTTPClient(ABC):
    """
    Represents a HTTP client.
    """

    __slots__ = ("session", "city_data", "proxy")

    @staticmethod
    def format_datetime(date: datetime) -> str:
        """
        Formats the datetime.

        :param datetime date: The datetime.
        :return: The formatted datetime
        :rtype: str
        """

        return date.strftime("%d.%m.%Y")

    @staticmethod
    def parse_response(response: str) -> Any:
        """
        Parses the API response.

        :param str response: The response.
        :raises: AccessDenied: You cannot access the pikudhaoref API from outside Israel.
        :return: The parsed response.
        :rtype: Optional[Dict]
        """

        if "Access Denied" in response:
            raise AccessDenied(
                "You cannot access the pikudhaoref API from outside Israel."
            )

        try:
            return json.loads(response)
        except json.decoder.JSONDecodeError:
            return {}

    def request(self, method: str, url: str, headers: Dict[str, str] = None) -> Any:
        """
        |maybecoro|

        Sends a request to the URL with the method.

        :param str method: The method.
        :param Dict[str, str] headers: The headers.
        :param str url: The URL.
        :return: The parsed response.
        :rtype: Optional[Dict]
        """

    @staticmethod
    def _format_city_data(dictionary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Formats the city data.

        :param Dict[str, Any] dictionary: The dictionary.
        :return: The formatted city data.
        :rtype: List[Dict[str, Any]]
        """

        areas = dictionary["areas"]
        cities = list(dictionary["cities"].values())

        for city in cities:
            city.pop("id")
            city["area"] = areas[str(city["area"])]

        return cities

    @abstractmethod
    def initialize_city_data(self) -> None:
        """
        |maybecoro|

        Initializes the city data.

        :return: None
        :rtype: None
        """

    @abstractmethod
    def get_history(self, mode: int) -> List[dict]:
        """
        |maybecoro|

        Returns the history of sirens in the specific mode.

        :param int mode: The mode.
        :return: The list of sirens.
        :rtype: List[dict]
        """

    def get_range_history(self, start: datetime, end: datetime) -> List[dict]:
        """
        |maybecoro|

        Returns the history of sirens in the range.

        :param datetime start: The start.
        :param datetime end: The end.
        :return: The list of sirens.
        :rtype: List[dict]
        """

    @abstractmethod
    def get_current_sirens(self) -> List[str]:
        """
        |maybecoro|

        Returns the current sirens.

        :return: The list of city names.
        :rtype: List[str]
        """


class Client(ABC, EventManager):
    """
    Represents a client
    """

    __slots__ = (
        "closed",
        "http",
        "update_interval",
        "_known_sirens",
        "city_cache",
        "_initialized",
    )

    @staticmethod
    def remove_duplicates(list_: list) -> list:
        """
        Removes duplicate elements from the list.

        :param list list_: The list.
        :return: The removed duplicate list.
        :rtype: list
        """

        return list(dict.fromkeys(list_))  # Nice little cheat

    def get_city(self, city_name: str) -> City | str:
        # Get from city cache
        for city in self.city_cache:
            if city_name == city or city_name in city.name.languages:
                return city

        # Create an instance
        city = City.from_city_name(city_name, self.http.city_data)
        self.city_cache.append(city)
        return city
