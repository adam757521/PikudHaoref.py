from __future__ import annotations

import asyncio
import time
from datetime import datetime
from threading import Thread
from typing import Union, List, TYPE_CHECKING

from .abc import Client
from .enums import HistoryMode
from .http import SyncHTTPClient, AsyncHTTPClient
from .siren import Siren

if TYPE_CHECKING:
    from .range import Range

__all__ = ("SyncClient", "AsyncClient")


class SyncClient(Client):
    """
    Represents a sync pikudhaoref client.
    """

    __slots__ = (
        "closed",
        "http",
        "update_interval",
        "_known_sirens",
        "city_cache",
        "_initialized",
    )

    def __init__(self, update_interval: Union[int, float] = 2, proxy: str = None):
        """
        :param Union[int, float] update_interval: The update interval of the client.
        """

        super().__init__()

        self.closed = False
        self.http = SyncHTTPClient(proxy=proxy)

        self.update_interval = update_interval
        self._known_sirens = []
        self.city_cache = []
        self._initialized = False
        self.initialize()

        Thread(target=self._handle_sirens, daemon=True).start()

    def initialize(self):
        if not self._initialized:
            for city in self.http.city_data:
                self.city_cache.append(self.get_city(city["he"]))

            self._initialized = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.closed = True
        self.http.session.close()

    def get_history(
        self, mode: HistoryMode = HistoryMode.TODAY, date_range: Range = None
    ) -> List[Siren]:
        if date_range:
            sirens = self.http.get_range_history(date_range.start, date_range.end)
        else:
            sirens = self.http.get_history(mode.value)

        return [Siren.from_raw(x) for x in sirens]

    @property
    def current_sirens(self) -> List[Siren]:
        return [
            Siren(self.get_city(x), datetime.utcnow())
            for x in self.remove_duplicates(self.http.get_current_sirens())
        ]

    def _handle_sirens(self):
        self.initialize()

        while not self.closed:
            time.sleep(self.update_interval)
            sirens = self.current_sirens

            new_sirens = [
                siren
                for siren in sirens
                if siren.city not in [siren.city for siren in self._known_sirens]
            ]
            if new_sirens:
                self.call_sync_event("on_siren", new_sirens)

            ended_sirens = [
                x
                for x in self._known_sirens
                if x.city not in [siren.city for siren in sirens]
            ]
            if ended_sirens:
                self.call_sync_event("on_siren_end", ended_sirens)

            self._known_sirens = sirens


class AsyncClient(Client):
    """
    Represents an async pikudhaoref client.
    """

    __slots__ = ("loop",)

    def __init__(
        self,
        update_interval: Union[int, float] = 2,
        loop: asyncio.AbstractEventLoop = None,
        proxy: str = None,
    ):
        """
        :param Union[int, float] update_interval: The update interval of the client.
        """

        super().__init__()

        self.loop = loop or asyncio.get_event_loop()
        self.closed = False
        self.http = AsyncHTTPClient(loop=loop, proxy=proxy)

        self._initialized = False
        self.city_cache = []
        self.update_interval = update_interval
        self._known_sirens = []

        loop.create_task(self._handle_sirens())

    async def initialize(self):
        if not self._initialized:
            await self.http.initialize_city_data()

            for city in self.http.city_data:
                self.city_cache.append(self.get_city(city["he"]))

            self._initialized = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.closed = True
        await self.http.session.close()

    async def get_history(
        self, mode: HistoryMode = HistoryMode.TODAY, range_: Range = None
    ) -> List[Siren]:
        if range_:
            sirens = await self.http.get_range_history(range_.start, range_.end)
        else:
            sirens = await self.http.get_history(mode.value)

        return [Siren.from_raw(x) for x in sirens]

    async def current_sirens(self) -> List[Siren]:
        return [
            Siren(self.get_city(x), datetime.utcnow())
            for x in self.remove_duplicates(await self.http.get_current_sirens())
        ]

    async def _handle_sirens(self):
        await self.initialize()

        while not self.closed:
            await asyncio.sleep(self.update_interval)
            sirens = await self.current_sirens()

            new_sirens = [
                siren
                for siren in sirens
                if siren.city not in [siren.city for siren in self._known_sirens]
            ]
            if new_sirens:
                await self.call_async_event("on_siren", new_sirens)

            ended_sirens = [
                x
                for x in self._known_sirens
                if x.city not in [siren.city for siren in sirens]
            ]
            if ended_sirens:
                await self.call_async_event("on_siren_end", ended_sirens)

            self._known_sirens = sirens
