import time
from src.models.type_models import (
    TelemetryData,
    Event,
    EventTypeEnum,
    TelemetryEventsEnum,
    KeyInputEvent,
    MouseInputEvent,
)
from src.runtime.core.logger import LOGGER
from ..core.event_bus import EVENT_BUS


class TelemetryManager:
    """Central hub for performance metrics and input tracking."""

    _instance = None
    data: TelemetryData

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.data = TelemetryData()
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._register_listeners()
        self._initialized = True

    def _register_listeners(self):
        EVENT_BUS.subscribe(TelemetryEventsEnum.UPDATE, self._handle_telemetry_update)
        EVENT_BUS.subscribe(EventTypeEnum.INPUT, self._handle_input_metrics)

    def _handle_telemetry_update(self, event: Event):
        if not isinstance(event.data, TelemetryData):
            return

        new_data: TelemetryData = event.data

        # FPS
        if new_data.fps is not None:
            self.data.fps = new_data.fps

        # Terminal Latency
        if new_data.latency_ms is not None:
            self.data.latency_ms = new_data.latency_ms

        # Last Key
        if new_data.last_key is not None:
            self.data.last_key = new_data.last_key

        # Mouse Position
        if new_data.mouse_pos is not None:
            self.data.mouse_pos = new_data.mouse_pos

        # Hitboxes
        if new_data.active_hitboxes is not None:
            self.data.active_hitboxes = new_data.active_hitboxes

    def _handle_input_metrics(self, event: Event):
        now: float = time.perf_counter()

        if isinstance(event.data, (KeyInputEvent, MouseInputEvent)):
            # Transit Latency: Hardware Arrival -> Event Processing
            if event.data.timestamp > 0:
                self.data.latency_ms = (now - event.data.timestamp) * 1000

        if isinstance(event.data, KeyInputEvent):
            self.data.last_key = (
                event.data.key.name
                if event.data.is_special
                else (event.data.char or "None")
            )
        elif isinstance(event.data, MouseInputEvent):
            self.data.mouse_pos = (event.data.x, event.data.y)


TELEMETRY_MANAGER = TelemetryManager()
