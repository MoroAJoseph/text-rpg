from typing import Callable, TYPE_CHECKING, TypeVar, Any
from enum import Enum
from ..core import EventData, EventTypeEnum

if TYPE_CHECKING:
    from ..kernel import Engine

TName = TypeVar("TName", bound=Enum)


class EventsAPI:
    """Public interface for event emission and subscription."""

    def __init__(self, engine: "Engine"):
        self._bus = engine.ctx.bus

    def emit(self, event: EventData[Any, Any]):
        """Queue an event into the bus."""
        self._bus.emit(event)

    def on(self, name: TName, callback: Callable[[EventData[TName, Any]], None]):
        """Subscribe to a specific event name (e.g., KeyInputEnum.SPACE)."""
        self._bus.subscribe_to_name(name, callback)

    def on_type(
        self, etype: EventTypeEnum, callback: Callable[[EventData[Any, Any]], None]
    ):
        """Subscribe to a category (e.g., EventTypeEnum.INPUT)."""
        self._bus.subscribe_to_type(etype, callback)
