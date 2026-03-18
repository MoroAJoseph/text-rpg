from typing import Callable, TYPE_CHECKING, TypeVar, Any
from enum import Enum
from ..core import EventData

if TYPE_CHECKING:
    from ..core import Engine

# TName represents any Enum (KeyInputEnum, SystemEventEnum, or UserEnum)
TName = TypeVar("TName", bound=Enum)


class EventsAPI:
    """Public interface for domain-agnostic event emission and subscription."""

    def __init__(self, engine: "Engine"):
        self._bus = engine.ctx.bus

    def emit(self, event: EventData[Any, Any]):
        """Passes a generic EventData packet to the Event Bus."""
        self._bus.emit(event)

    def on(self, event_name: TName, callback: Callable[[EventData[TName, Any]], None]):
        """
        Subscribe to a specific event name.

        :param event_name: The Enum member to watch (e.g., KeyInputEnum.SPACE).
        :param callback: Function called when the event occurs.
        """
        self._bus.subscribe(event_name, callback)
