from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import requests
import json
import aiohttp
import asyncio

from .exceptions import AccessDenied

if TYPE_CHECKING:
    from datetime import datetime

__all__ = ("HTTPClient", "SyncHTTPClient", "AsyncHTTPClient")


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

        if response == "":  # ...
            return {}

        return json.loads(response)

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


class SyncHTTPClient(HTTPClient):
    def __init__(self, session: requests.Session = None, proxy: str = None):
        self.session = session or requests.Session()
        self.city_data = {}
        self.proxy = proxy
        self.initialize_city_data()

    def request(self, method: str, url: str, headers: Dict[str, str] = None) -> Any:
        r = self.session.request(
            method,
            url,
            headers=headers or {},
            proxies=self.proxy and {"http": f"http://{self.proxy}/"},
        )
        return self.parse_response(r.text)

    def initialize_city_data(self) -> None:
        self.city_data = self._format_city_data(
            self.request("GET", "https://www.tzevaadom.co.il/static/cities.json")
        )

    def get_history(self, mode: int) -> List[dict]:
        return self.request(
            "GET",
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode={mode}",
        )

    def get_range_history(self, start: datetime, end: datetime) -> List[dict]:
        start = self.format_datetime(start)
        end = self.format_datetime(end)

        return self.request(
            "GET",
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode=0&fromDate={start}&toDate={end}",
        )

    def get_current_sirens(self) -> List[str]:
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.oref.org.il/",
        }

        return self.request(
            "GET",
            "https://www.oref.org.il/WarningMessages/Alert/alerts.json",
            headers=headers,
        ).get("data", [])


class AsyncHTTPClient(HTTPClient):
    def __init__(
        self,
        session: aiohttp.ClientSession = None,
        loop: asyncio.BaseEventLoop = None,
        proxy: str = None,
    ):
        self.session = session or aiohttp.ClientSession(loop=loop)
        self.proxy = proxy
        self.city_data = {}

    async def request(
        self, method: str, url: str, headers: Dict[str, str] = None
    ) -> Any:
        r = await self.session.request(
            method,
            url,
            headers=headers or {},
            proxy=self.proxy and f"http://{self.proxy}/",
        )
        return self.parse_response(await r.text())

    async def initialize_city_data(self) -> None:
        self.city_data = self._format_city_data(
            await self.request("GET", "https://www.tzevaadom.co.il/static/cities.json")
        )

    async def get_history(self, mode: int) -> List[dict]:
        return await self.request(
            "GET",
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode={mode}",
        )

    async def get_range_history(self, start: datetime, end: datetime):
        start = self.format_datetime(start)
        end = self.format_datetime(end)

        return await self.request(
            "GET",
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode=0&fromDate={start}&toDate={end}",
        )

    async def get_current_sirens(self) -> List[str]:
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.oref.org.il/",
        }

        return (
            await self.request(
                "GET",
                "https://www.oref.org.il/WarningMessages/Alert/alerts.json",
                headers=headers,
            )
        ).get("data", [])
