import time
from typing import Dict, List, Optional, Union

from engine.core import (
    EventData,
    EngineEventBus,
    EventTypeEnum,
    DomainManager,
)

from .provider import InputProvider
from .telemetry import InputTelemetry
from .enums import (
    InputEventEnum,
    InputStateEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
)
from .dataclasses import InputEvent, InputEventData, InputIdentifier


class InputManager(DomainManager):
    """
    Orchestrates input hardware polling and state normalization.

    Acts as a bridge between low-level drivers (Providers) and the Engine Bus.
    Handles 'Key Decay' to synthesize RELEASED states for terminal environments
    that do not provide native key-up events.
    """

    def __init__(self, bus: EngineEventBus):
        self._bus: EngineEventBus = bus
        self._providers: List[InputProvider] = []

        # Tracks the current state of every input identifier (Key, Mouse, or Scroll)
        self._key_states: Dict[InputIdentifier, InputStateEnum] = {}

        # Tracking for decay logic (Time since last 'PRESSED' signal)
        self._key_timers: Dict[InputIdentifier, float] = {}
        self._decay_threshold: float = 0.12

        self.telemetry = InputTelemetry(bus=self._bus)

    def update(self, dt: float):
        """
        Processes one engine frame of input.

        Args:
            dt (float): Delta time since the last frame.
        """
        start = time.perf_counter()
        total_new_events = 0

        # 1. Handle synthetic releases for keys that haven't been 'refreshed'
        self._handle_key_decay(dt)

        # 2. Poll all registered hardware providers
        for provider in self._providers:
            events: List[InputEvent] = provider.poll()
            total_new_events += len(events)

            for event in events:
                # Reset decay timer for this specific identifier
                self._key_timers[event.identifier] = 0.0
                self._process_input(event)

        # 3. Update telemetry metrics
        self.telemetry.record_poll(start, total_new_events)
        self.telemetry.update_state(len(self._key_states))

    def add_provider(self, provider: InputProvider):
        """Registers a new hardware input source."""
        self._providers.append(provider)

    def shutdown(self):
        """Cleans up all providers and state tracking."""
        self._providers.clear()
        self._key_states.clear()
        self._key_timers.clear()

    def _handle_key_decay(self, dt: float):
        """Synthesizes RELEASED events for keys exceeding the decay threshold."""
        keys_to_release = []
        for identifier, elapsed in self._key_timers.items():
            new_elapsed = elapsed + dt
            self._key_timers[identifier] = new_elapsed

            if new_elapsed > self._decay_threshold:
                # Only release if it's currently marked as PRESSED or HELD
                if self._key_states.get(identifier) != InputStateEnum.RELEASED:
                    keys_to_release.append(identifier)

        for identifier in keys_to_release:
            self._emit_synthetic_event(identifier, InputStateEnum.RELEASED)
            # Remove from timers to stop tracking until next press
            self._key_timers.pop(identifier, None)

    def _process_input(self, event: InputEvent):
        """
        Normalizes input and performs double-emission for routing.
        """
        # Ignore redundant state changes (e.g., multiple PRESSED signals)
        current_state: Optional[InputStateEnum] = self._key_states.get(event.identifier)
        if current_state == event.state:
            return

        self._key_states[event.identifier] = event.state

        # Determine Category for EventData.name
        if isinstance(event.identifier, KeyInputEnum):
            category = InputEventEnum.KEYBOARD
        elif isinstance(event.identifier, MouseInputEnum):
            category = InputEventEnum.MOUSE
        elif isinstance(event.identifier, ScrollInputEnum):
            category = InputEventEnum.SCROLL
        else:
            return

        # Double Emission:
        # 1. Emit to Category (e.g., InputEventEnum.KEYBOARD)
        # 2. Emit to Specific Identifier (e.g., KeyInputEnum.SPACE)
        self._emit_to_bus(category, event)
        self._emit_to_bus(event.identifier, event)

    def _emit_synthetic_event(self, identifier: InputIdentifier, state: InputStateEnum):
        """Synthesizes a state change event (usually RELEASED)."""
        self._key_states[identifier] = state

        event = InputEvent(
            identifier=identifier,
            state=state,
            timestamp=time.time(),
            raw_data="synthetic_decay",
        )

        # Determine Category
        if isinstance(identifier, KeyInputEnum):
            cat = InputEventEnum.KEYBOARD
        elif isinstance(identifier, MouseInputEnum):
            cat = InputEventEnum.MOUSE
        else:
            cat = InputEventEnum.SCROLL

        self._emit_to_bus(cat, event)
        self._emit_to_bus(identifier, event)

    def _emit_to_bus(
        self, routing_name: Union[InputEventEnum, InputIdentifier], event: InputEvent
    ):
        """Helper to wrap data in the standard Engine Packet format."""
        packet = EventData(type=EventTypeEnum.INPUT, name=routing_name, data=event)
        self._bus.emit(packet)
