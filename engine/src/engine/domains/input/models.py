from dataclasses import dataclass, field
import time
from typing import Any, Union
from engine.core.enums import EventTypeEnum
from engine.core.models import EventData, TickBucket
from engine.core.domain_protocols import DomainDriver
from .enums import (
    InputEventNameEnum,
    InputStateEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
)

# ---
# --- Generic
# ---


InputIdentifier = Union[KeyInputEnum, MouseInputEnum, ScrollInputEnum]


@dataclass
class InputPayload:
    """
    The actual hardware data.

    :param identifier:InputIdentifier
    :param state: InputStateEnum
    :param timestamp: float
    :param coords: tuple[int, int] = (0, 0)
    :param raw_data: Any = None
    """

    identifier: InputIdentifier
    state: InputStateEnum
    timestamp: float
    coords: tuple[int, int] = (0, 0)
    raw_data: Any = None


@dataclass
class InputSpoke:
    """
    Internal container used by the InputManager to orchestrate
    different poll rates for different hardware drivers.
    """

    driver: DomainDriver
    bucket: TickBucket
    capability_name: str


@dataclass
class InputEvent(EventData[InputEventNameEnum, InputPayload]):
    """
    A strictly typed Input Packet.
    Forces the 'type' to be EventTypeEnum.INPUT.
    """

    type: EventTypeEnum = field(default=EventTypeEnum.INPUT, init=False)


# ---
# --- Telemetry
# ---


@dataclass
class InputMetrics:
    """Telemetry snapshot for the input domain."""

    last_poll_duration: float = 0.0
    total_events_processed: int = 0
    active_keys_count: int = 0
    active_mouse_buttons_count: int = 0


@dataclass
class InputTelemetryPayload:
    """The data bundle for a telemetry broadcast."""

    metrics: InputMetrics
    timestamp: float = field(default_factory=time.perf_counter)


@dataclass
class InputTelemetryEvent(EventData[InputEventNameEnum, InputTelemetryPayload]):
    """
    A specialized event for Input Domain performance data.
    """

    type: EventTypeEnum = field(default=EventTypeEnum.INPUT, init=False)
    name: InputEventNameEnum = field(default=InputEventNameEnum.TELEMETRY, init=False)
