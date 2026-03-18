from dataclasses import dataclass
from typing import Any, Union
from engine.core import EventData
from .enums import (
    InputEventEnum,
    InputStateEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
)


InputIdentifier = Union[KeyInputEnum, MouseInputEnum, ScrollInputEnum]


@dataclass
class InputEvent:
    """
    Normalized hardware input data encompassing keyboard, mouse, and scroll.
    """

    identifier: InputIdentifier
    state: InputStateEnum
    timestamp: float
    coords: tuple[int, int] = (0, 0)
    raw_data: Any = None


@dataclass
class InputMetrics:
    """Telemetry snapshot for the input domain."""

    last_poll_duration: float = 0.0
    total_events_processed: int = 0
    active_keys_count: int = 0
    active_mouse_buttons_count: int = 0


# The standardized packet for the Input Domain
InputEventData = EventData[InputEventEnum, Any]
