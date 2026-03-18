import time

from engine.core import EventTypeEnum, EngineEventBus
from .enums import InputEventEnum
from .dataclasses import InputEventData, InputMetrics


class InputTelemetry:
    """Tracks performance and density of the input domain."""

    def __init__(self, bus: EngineEventBus):
        self.metrics = InputMetrics()
        self._bus: EngineEventBus[InputEventEnum] = bus

    def record_poll(self, start_time: float, event_count: int):
        self.metrics.last_poll_duration = time.perf_counter() - start_time
        self.metrics.total_events_processed += event_count

    def update_state(self, key_count: int):
        self.metrics.active_keys_count = key_count

    def _emit_metrics(self):
        """Broadcasts current performance data to the engine."""
        event = InputEventData(
            type=EventTypeEnum.INPUT,
            name=InputEventEnum.TELEMETRY,
            data=self.metrics,
        )
        self._bus.emit(event)
