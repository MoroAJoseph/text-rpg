import time
from typing import TYPE_CHECKING

from .models import InputMetrics, InputTelemetryEvent, InputTelemetryPayload

if TYPE_CHECKING:
    from engine.core.bus import EventBus


class InputTelemetry:
    """Tracks performance and density of the input domain."""

    def __init__(self, bus: "EventBus", report_interval: float = 1.0):
        self.metrics = InputMetrics()
        self._bus = bus
        self._report_interval = report_interval
        self._last_report_time = time.perf_counter()

    def record_poll(self, start_time: float, event_count: int):
        """Updates timing and throughput metrics and checks for broadcast."""
        self.metrics.last_poll_duration = time.perf_counter() - start_time
        self.metrics.total_events_processed += event_count

        now = time.perf_counter()
        if now - self._last_report_time >= self._report_interval:
            self._emit_metrics()
            self._last_report_time = now

    def update_state(self, key_count: int, mouse_count: int):
        """Updates the current state counts from the InputManager."""
        self.metrics.active_keys_count = key_count
        self.metrics.active_mouse_buttons_count = mouse_count

    def _emit_metrics(self):
        """Broadcasts the specialized Telemetry Event."""
        # Wrap metrics in the specific payload
        payload = InputTelemetryPayload(metrics=self.metrics)

        # Instantiate the specialized event
        event = InputTelemetryEvent(data=payload)

        self._bus.emit(event)
