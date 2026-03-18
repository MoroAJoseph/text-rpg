from __future__ import annotations
from typing import List, Protocol, Dict, Any

from ..common.enums import KeyInputEnum, InputStateEnum, EventTypeEnum
from ..common.dataclasses import InputEvent, EventData
from ..core.event_bus import EngineEventBus


class InputProvider(Protocol):
    """Interface for input drivers (Blessed, Pygame, etc.)"""

    def poll(self) -> List[InputEvent]: ...


class InputManager:
    """Orchestrates input from various providers and pushes to the injected bus."""

    def __init__(self, bus: EngineEventBus):
        self._bus = bus
        self._providers: List[InputProvider] = []
        # Track state to prevent duplicate event emissions
        self._key_states: Dict[KeyInputEnum, InputStateEnum] = {}

    def register_provider(self, provider: InputProvider):
        """Adds an input driver to the polling list."""
        self._providers.append(provider)

    def update(self):
        """Called every frame by the main loop to poll drivers."""
        for provider in self._providers:
            events = provider.poll()
            for event in events:
                self._process_input(event)

    def _process_input(self, event: InputEvent):
        """Internal filter to handle de-duplication and bus emission."""
        current_state = self._key_states.get(event.key)

        # Only emit if the state actually changed
        if current_state == event.state:
            return

        self._key_states[event.key] = event.state

        # Emit to the SPECIFIC injected bus instance
        engine_event = EventData(type=EventTypeEnum.INPUT, name=event.key, data=event)
        self._bus.emit(engine_event)
