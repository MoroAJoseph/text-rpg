import time
from typing import Dict, List, Optional, Any

from engine.core.bus import EventBus
from engine.config.models import InputConfig
from engine.core.domain_protocols import DomainManager

from .models import (
    InputEvent,
    InputPayload,
    InputIdentifier,
    InputSpoke,
)
from .enums import (
    InputStateEnum,
    ScrollInputEnum,
    InputEventNameEnum,
    MouseInputEnum,
)
from .telemetry import InputTelemetry


class InputManager(DomainManager):
    """Orchestrates hardware drivers and maintains global input state."""

    def __init__(self, config: InputConfig):
        self.config = config
        self._spokes: List[InputSpoke] = []

        # State Tracking
        self._key_states: Dict[InputIdentifier, InputStateEnum] = {}
        self._key_timers: Dict[InputIdentifier, float] = {}
        self._key_metadata: Dict[InputIdentifier, Any] = {}
        self._decay_threshold = config.decay_threshold

        # Telemetry
        self._bus: Optional[EventBus] = None
        self.telemetry: Optional[InputTelemetry] = None

    def register_bus(self, bus: EventBus) -> None:
        """Hooks the manager into the system event pipeline."""
        self._bus = bus
        self.telemetry = InputTelemetry(bus)

    def add_spoke(self, name: str, driver: Any, rate: float):
        """Attaches a hardware driver with a specific polling frequency."""
        from engine.core.models import TickBucket

        bucket = TickBucket(name=f"input_{name}", target_rate=rate)
        self._spokes.append(
            InputSpoke(driver=driver, bucket=bucket, capability_name=name)
        )

    def update(self, dt: float):
        """Main domain loop: Decays keys, polls drivers, and records telemetry."""
        if not self._bus or not self.telemetry:
            return

        poll_start = time.perf_counter()
        events_processed = 0

        # Age existing input states
        self._handle_key_decay(dt)

        # Poll hardware spokes
        for spoke in self._spokes:
            spoke.bucket.accumulator += dt

            # Process as many ticks as accumulated (catch-up logic)
            while spoke.bucket.accumulator >= spoke.bucket.interval:
                payloads = spoke.driver.poll()
                events_processed += len(payloads)

                for payload in payloads:
                    # Reset decay timer on any hardware activity
                    self._key_timers[payload.identifier] = 0.0
                    self._process_input(payload)

                spoke.bucket.accumulator -= spoke.bucket.interval

        # Update Metrics
        active_keys = [
            k for k, v in self._key_states.items() if v != InputStateEnum.RELEASED
        ]
        keys_count = sum(1 for k in active_keys if not isinstance(k, MouseInputEnum))
        mouse_count = sum(1 for k in active_keys if isinstance(k, MouseInputEnum))

        self.telemetry.update_state(keys_count, mouse_count)
        self.telemetry.record_poll(poll_start, events_processed)

    def _process_input(self, payload: InputPayload):
        """Maps raw hardware payloads to internal state and bus events."""
        # Determine event category
        event_name = InputEventNameEnum.KEYBOARD
        if isinstance(payload.identifier, MouseInputEnum):
            event_name = InputEventNameEnum.MOUSE
        elif isinstance(payload.identifier, ScrollInputEnum):
            # Scroll is transient; no state tracking or decay
            self._emit_to_bus(InputEventNameEnum.SCROLL, payload)
            return

        current = self._key_states.get(payload.identifier)

        # Logical Promotion: PRESSED -> HELD if already active
        if (
            current in (InputStateEnum.PRESSED, InputStateEnum.HELD)
            and payload.state == InputStateEnum.PRESSED
        ):
            payload.state = InputStateEnum.HELD

        # Deduplication: Don't emit if state hasn't changed
        if current == payload.state:
            return

        # Commit State
        self._key_metadata[payload.identifier] = payload.raw_data
        self._key_states[payload.identifier] = payload.state
        self._emit_to_bus(event_name, payload)

    def _handle_key_decay(self, dt: float):
        """Forces RELEASED state for keys that haven't reported in recently."""
        released_list = []

        # Increment all active timers
        for ident in list(self._key_timers.keys()):
            self._key_timers[ident] += dt
            if (
                self._key_timers[ident] > self._decay_threshold
                and self._key_states.get(ident) != InputStateEnum.RELEASED
            ):
                released_list.append(ident)

        for ident in released_list:
            self._key_states[ident] = InputStateEnum.RELEASED
            self._emit_synthetic(ident, InputStateEnum.RELEASED)
            # Cleanup timer to stop incrementing it
            self._key_timers.pop(ident, None)

    def _emit_synthetic(self, ident: InputIdentifier, state: InputStateEnum):
        """Generates a software-level event (e.g., timeout release)."""
        name = (
            InputEventNameEnum.MOUSE
            if isinstance(ident, MouseInputEnum)
            else InputEventNameEnum.KEYBOARD
        )
        raw = self._key_metadata.get(ident, "decay")
        payload = InputPayload(
            identifier=ident, state=state, timestamp=time.perf_counter(), raw_data=raw
        )
        self._emit_to_bus(name, payload)

    def _emit_to_bus(self, name: InputEventNameEnum, payload: InputPayload):
        """Standard wrapper for bus emission."""
        if self._bus:
            self._bus.emit(InputEvent(name=name, data=payload))

    def shutdown(self):
        """Graceful teardown of all hardware drivers."""
        for spoke in self._spokes:
            spoke.driver.shutdown()
