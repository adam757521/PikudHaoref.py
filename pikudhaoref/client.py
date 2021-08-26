from threading import Thread
from typing import (
    Union,
    List
)

from .base import EventManager
import json
import time
import requests


class Client(EventManager):
    def __init__(self, update_interval: Union[int, float] = 2):
        super().__init__()
        self.update_interval = update_interval
        self._known_sirens = []
        Thread(target=self._handle_sirens).start()

    @staticmethod
    def history() -> List[dict]:
        website_content = requests.get("https://www.oref.org.il/WarningMessages/History/AlertsHistory.json").text

        return [x for x in json.loads(website_content)] if website_content != "\r\n" else []

    @staticmethod
    def get_current_sirens() -> List[str]:
        website_content = requests.get("https://www.oref.org.il/WarningMessages/Alert/alerts.json",
                                       headers={"X-Requested-With": "XMLHttpRequest",
                                                "Referer": "https://www.oref.org.il/"}).text

        return json.loads(website_content)["data"] if website_content != "" else []

    def _handle_sirens(self):
        while True:
            time.sleep(self.update_interval)
            cities = self.get_current_sirens()

            if cities:
                new_cities = [city for city in cities if city not in self._known_sirens]
                if new_cities:
                    self.call_event('on_siren', new_cities)

                ended_sirens = [x for x in self._known_sirens if x not in cities]
                if ended_sirens:
                    self.call_event("on_siren_end", ended_sirens)

                self._known_sirens = cities
            else:
                self._known_sirens = []
