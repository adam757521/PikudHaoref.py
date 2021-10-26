from __future__ import annotations

from enum import Enum

__all__ = ("HistoryMode",)


class HistoryMode(Enum):
    RANGE = 0
    TODAY = 1
    LAST_WEEK = 2
    LAST_MONTH = 3
