from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from .enums import EventTypeEnum, SystemEventEnum

TEventName = TypeVar("TEventName", bound=Enum)
DEventData = TypeVar("DEventData")


@dataclass
class EventData(Generic[TEventName, DEventData]):
    """The universal packet structure."""

    type: EventTypeEnum
    name: TEventName
    data: Optional[DEventData] = None


@dataclass
class TickBucket:
    """Temporal accumulator."""

    name: str
    target_rate: float
    accumulator: float = 0.0

    @property
    def interval(self) -> float:
        return 1.0 / self.target_rate if self.target_rate > 0 else float("inf")


SystemEvent = EventData[SystemEventEnum, Any]
