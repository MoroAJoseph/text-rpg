from enum import Enum
from typing import TypeVar, Any

from .base_bus import BaseEventBus
from ..dataclasses import EventData

TName = TypeVar("TName", bound=Enum)
TData = TypeVar("TData")


class EngineEventBus(BaseEventBus[TName, EventData[TName, Any]]):
    """
    A domain-agnostic event bus.
    Routes EventData packets using the Enum member as the key.
    """

    def _get_event_name(self, event: EventData[TName, Any]) -> TName:
        return event.name
