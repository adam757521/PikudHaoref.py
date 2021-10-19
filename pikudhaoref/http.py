from abc import ABC, abstractmethod
from typing import List
import requests
import json
import aiohttp
import asyncio


__all__ = ("HTTPClient", "SyncHTTPClient", "ASyncHTTPClient")


class HTTPClient(ABC):
    """
    Represents a HTTP client.
    """

    __slots__ = ("session",)

    @abstractmethod
    def get_history(self) -> List[dict]:
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

    def get_history(self) -> List[dict]:
        website_content = self.session.get(
            "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
        ).text

        if website_content == "\r\n":
            return []

        return json.loads(website_content)

    def get_current_sirens(self) -> List[str]:
        website_content = self.session.get(
            "https://www.oref.org.il/WarningMessages/Alert/alerts.json",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.oref.org.il/",
            },
        ).text

        return json.loads(website_content)["data"] if website_content != "" else []


class ASyncHTTPClient(HTTPClient):
    def __init__(
        self, session: aiohttp.ClientSession = None, loop: asyncio.BaseEventLoop = None
    ):
        self.session = session or aiohttp.ClientSession(loop=loop)

    async def get_history(self) -> List[dict]:
        r = await self.session.get(
            "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
        )

        website_content = await r.text()

        if website_content == "\r\n":
            return []

        return json.loads(website_content)

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
