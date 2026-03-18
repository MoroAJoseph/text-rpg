from typing import Callable, TYPE_CHECKING, TypeVar, Any
from enum import Enum
from ..core import EventData, EventTypeEnum

if TYPE_CHECKING:
    from ..core import Engine

TName = TypeVar("TName", bound=Enum)


class EventsAPI:
    """Public interface for domain-agnostic event emission and subscription."""

    def __init__(self, engine: "Engine"):
        self._engine = engine
        self._bus = engine.ctx.bus

    def emit(self, event: EventData[Any, Any]):
        self._bus.emit(event)

    def on(self, event_name: TName, callback: Callable[[EventData[TName, Any]], None]):
        """Subscribe to a specific event name (e.g., KeyInputEnum.SPACE)."""
        self._bus.subscribe(event_name, callback)

    def on_type(
        self, event_type: EventTypeEnum, callback: Callable[[EventData[Any, Any]], None]
    ):
        """
        Subscribe to an entire category of events (e.g., EventTypeEnum.INPUT).
        Implemented via a proxy subscriber that filters by the 'type' field.
        """

        def proxy_callback(event: EventData[Any, Any]):
            if event.type == event_type:
                callback(event)

        # We attach this to a 'Global' or 'System' tick to ensure it checks
        # every event passing through the bus, or we modify the Bus to support
        # type-based indexing. For now, we'll use a direct internal proxy.
        self._bus.subscribe_to_type(event_type, callback)
