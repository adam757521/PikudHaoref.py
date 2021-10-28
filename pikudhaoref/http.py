from __future__ import annotations

from typing import List, Dict, Any, TYPE_CHECKING
import requests
import aiohttp
import asyncio

from .abc import HTTPClient

if TYPE_CHECKING:
    from datetime import datetime

__all__ = ("SyncHTTPClient", "AsyncHTTPClient")


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
