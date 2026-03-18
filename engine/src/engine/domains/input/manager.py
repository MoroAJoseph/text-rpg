import time
from typing import Dict, Optional
from engine.core import (
    EventData,
    EngineEventBus,
    EventTypeEnum,
    DomainManager,
    DomainDriver,
)
from .telemetry import InputTelemetry
from .enums import InputStateEnum, ScrollInputEnum
from .dataclasses import InputEvent, InputIdentifier


class InputManager(DomainManager):
    """Orchestrates hardware polling and key-decay synthesis."""

    def __init__(self):
        self._bus: Optional[EngineEventBus] = None
        self.driver: Optional[DomainDriver] = None
        self.telemetry: Optional[InputTelemetry] = None

        self._key_states: Dict[InputIdentifier, InputStateEnum] = {}
        self._key_timers: Dict[InputIdentifier, float] = {}
        self._key_metadata: Dict[InputIdentifier, str] = {}
        self._decay_threshold: float = 0.12  # TODO: get from input options

    def register_bus(self, bus: EngineEventBus) -> None:
        self._bus = bus
        self.telemetry = InputTelemetry(bus=self._bus)

    def register_driver(self, driver: DomainDriver) -> None:
        self.driver = driver

    def update(self, dt: float):
        if not self._bus or not self.telemetry:
            return

        start = time.perf_counter()

        # 1. Decay keys (Synthesize RELEASED)
        self._handle_key_decay(dt)

        # 2. Poll Driver
        events = self.driver.poll() if self.driver else []
        for event in events:
            # Reset timer: this key is still physically active
            self._key_timers[event.identifier] = 0.0
            self._process_input(event)

        # 3. Telemetry
        self.telemetry.record_poll(start, len(events))
        self.telemetry.update_state(len(self._key_states))

    def _handle_key_decay(self, dt: float):
        """Releases keys that haven't been polled recently."""
        keys_to_release = []
        for identifier, elapsed in self._key_timers.items():
            new_elapsed = elapsed + dt
            self._key_timers[identifier] = new_elapsed

            if new_elapsed > self._decay_threshold:
                if self._key_states.get(identifier) != InputStateEnum.RELEASED:
                    keys_to_release.append(identifier)

        for identifier in keys_to_release:
            self._emit_synthetic_event(identifier, InputStateEnum.RELEASED)
            # Stop tracking the timer once released
            self._key_timers.pop(identifier, None)

    def _process_input(self, event: InputEvent):
        # Check if this is a scroll impulse
        if isinstance(event.identifier, ScrollInputEnum):
            # Scrolls are fire-and-forget. We don't track state or timers.
            self._emit_to_bus(event.identifier, event)
            return

        # Standard Key Logic (Press/Hold/Decay)
        current = self._key_states.get(event.identifier)

        if current == InputStateEnum.PRESSED and event.state == InputStateEnum.PRESSED:
            event.state = InputStateEnum.HELD

        if current == event.state:
            return

        self._key_metadata[event.identifier] = event.raw_data
        self._key_states[event.identifier] = event.state
        self._emit_to_bus(event.identifier, event)

    def _emit_synthetic_event(self, identifier: InputIdentifier, state: InputStateEnum):
        self._key_states[identifier] = state

        # NEW: Retrieve the character string instead of using "decay"
        raw = self._key_metadata.get(identifier, "unknown")

        event = InputEvent(
            identifier=identifier, state=state, timestamp=time.time(), raw_data=raw
        )

        self._emit_to_bus(identifier, event)

        # Cleanup metadata after release
        if state == InputStateEnum.RELEASED:
            self._key_metadata.pop(identifier, None)

    def _emit_to_bus(self, identifier: InputIdentifier, event: InputEvent):
        """Single point of emission. Routes by the specific identifier."""
        if self._bus:
            packet = EventData(type=EventTypeEnum.INPUT, name=identifier, data=event)
            self._bus.emit(packet)

    def shutdown(self):
        if self.driver:
            self.driver.shutdown()
        self._key_states.clear()
        self._key_timers.clear()
        self._key_metadata.clear()
