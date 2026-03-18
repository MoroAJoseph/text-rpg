from typing import Callable, TYPE_CHECKING
from ..common.enums import EventName
from ..common.dataclasses import EventData

if TYPE_CHECKING:
    from ..core.kernel import Engine


class EventsAPI:
    """Public interface for manual event emission and subscription."""

    def __init__(self, engine: "Engine"):
        self._bus = engine.ctx.bus

    def emit(self, event: EventData):
        """Passes a strictly typed EventData to the Event Bus."""
        self._bus.emit(event)

    def on(self, event_name: EventName, callback: Callable[[EventData], None]):
        """Subscribe to a specific event name."""
        self._bus.subscribe(event_name, callback)
