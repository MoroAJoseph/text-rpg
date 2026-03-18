from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from .enums import (
    EventTypeEnum,
    SystemEventEnum,
)


@dataclass
class InputOptions:
    enabled: bool = True
    driver: str = "blessed"  # The engine resolves this string later
    driver_args: dict = field(default_factory=dict)
    decay_threshold: float = 0.12

    def use_terminal(self, term):
        """Helper to make the dev script look clean."""
        self.driver_args["terminal"] = term
        return self


@dataclass
class EngineOptions:
    # Multi-Rate Logic
    rates: dict[str, float] = field(default_factory=dict)
    max_ticks_per_frame: int = 5

    # Domain Options
    input: InputOptions = field(default_factory=InputOptions)


@dataclass
class TickBucket:
    """An independent time accumulator for a specific frequency."""

    name: str
    target_rate: float
    accumulator: float = 0.0

    @property
    def interval(self) -> float:
        """The required time in seconds between pulses."""
        return 1.0 / self.target_rate if self.target_rate > 0 else float("inf")


# ---
# --- Events
# ---

TEventName = TypeVar("TEventName", bound=Enum)
DEventData = TypeVar("DEventData")


@dataclass
class EventData(Generic[TEventName, DEventData]):
    """The standard packet for all engine communication."""

    type: EventTypeEnum
    name: TEventName
    data: Optional[DEventData] = None


SystemEvent = EventData[SystemEventEnum, Any]
