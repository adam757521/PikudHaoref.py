from dataclasses import dataclass
from datetime import datetime

__all__ = ("Range",)


@dataclass
class Range:
    """
    Represents a date range.
    """

    start: datetime
    end: datetime
