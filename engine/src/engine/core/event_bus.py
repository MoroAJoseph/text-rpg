from ..common.event_bus import BaseEventBus
from ..common.enums import EventName
from ..common.dataclasses import EventData


class EngineEventBus(BaseEventBus[EventName, EventData]):
    """The specialized bus used by the Engine Kernel."""

    def _get_event_name(self, event: EventData) -> EventName:
        # Explicitly returning the Enum name from our EventData dataclass
        return event.name
