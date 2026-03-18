from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, List, Optional, TypeVar, Union

from .enums import (
    EventTypeEnum,
    InputStateEnum,
    KeyInputEnum,
    MouseInputEnum,
    SystemEventEnum,
)


@dataclass
class EngineOptions:
    # Basic Config
    width: int = 80
    height: int = 24

    # Feature Toggles (Scoping)
    use_input: bool = True
    use_audio: bool = False
    use_ui: bool = True

    # Addon support
    addons: List[Any] = field(default_factory=list)


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
InputEventData = EventData[Union[KeyInputEnum, MouseInputEnum], Any]


@dataclass
class InputEvent:
    """Normalized hardware input data."""

    key: KeyInputEnum
    state: InputStateEnum
    timestamp: float
    raw_data: Any = None  # Original char or mouse coords
