from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
import json
import aiohttp
import asyncio


__all__ = ("HTTPClient", "SyncHTTPClient", "AsyncHTTPClient")


class HTTPClient(ABC):
    """
    Represents a HTTP client.
    """

    __slots__ = ("session", "city_data")

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

        Returns the history of sirens in the last 24 hours.

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
    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self.city_data = {}
        self.initialize_city_data()

    def initialize_city_data(self) -> None:
        self.city_data = self._format_city_data(json.loads(self.session.get(
            f"https://www.tzevaadom.co.il/static/cities.json"
        ).text))

    def get_history(self, mode: int) -> List[dict]:
        return json.loads(self.session.get(
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode={mode}"
        ).text)

    def get_current_sirens(self) -> List[str]:
        website_content = self.session.get(
            "https://www.oref.org.il/WarningMessages/Alert/alerts.json",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.oref.org.il/",
            },
        ).text

        return json.loads(website_content)["data"] if website_content != "" else []


class AsyncHTTPClient(HTTPClient):
    def __init__(
        self, session: aiohttp.ClientSession = None, loop: asyncio.BaseEventLoop = None
    ):
        self.session = session or aiohttp.ClientSession(loop=loop)
        self.city_data = {}

    async def initialize_city_data(self) -> None:
        r = await self.session.get(f"https://www.tzevaadom.co.il/static/cities.json")

        website_content = await r.text()
        self.city_data = self._format_city_data(json.loads(website_content))

    async def get_history(self, mode: int) -> List[dict]:
        # https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate=12.10.2021&toDate=26.10.2021&mode=0
        r = await self.session.get(
            f"https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode={mode}"
        )

        return json.loads(await r.text())

    async def get_current_sirens(self) -> List[str]:
        r = await self.session.get(
            "https://www.oref.org.il/WarningMessages/Alert/alerts.json",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.oref.org.il/",
            },
        )

        website_content = await r.text()

        return json.loads(website_content)["data"] if website_content != "" else []
