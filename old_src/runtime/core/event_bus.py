from __future__ import annotations
from collections import defaultdict, deque
from typing import Callable, Dict, List
from old_src.models.type_models import Event, EventTypeEnum, UIEventsEnum
from old_src.runtime.core.logger import LOGGER


class EventBus:
    """Singleton event bus with double-buffered event queue."""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._listeners: Dict[object, List[Callable[[Event], None]]] = defaultdict(list)
        self._current_queue: deque[Event] = deque()
        self._next_queue: deque[Event] = deque()
        self._initialized = True

    # --- Listener Management ---
    def subscribe(self, event_name, callback: Callable[[Event], None]) -> None:
        self._listeners[event_name].append(callback)
        LOGGER.debug(f"{event_name} registered with {callback.__name__}")

    def unsubscribe(self, event_name, callback: Callable[[Event], None]) -> None:
        if callback in self._listeners.get(event_name, []):
            self._listeners[event_name].remove(callback)

    # --- Event Emission ---
    def emit(self, event: Event) -> None:
        """Queue an event for the next process cycle."""
        self._next_queue.append(event)

    # --- Event Processing ---
    def process(self) -> None:
        """
        Process all events in the current queue.
        Any new events emitted during processing go to the next queue.
        """
        # Swap queues
        self._current_queue, self._next_queue = self._next_queue, self._current_queue

        while self._current_queue:
            event = self._current_queue.popleft()
            for callback in self._listeners.get(event.name, []):
                if (
                    event.type != EventTypeEnum.TELEMETRY
                    and event.name != UIEventsEnum.RENDER
                ):
                    LOGGER.debug(f"Calling {event}")
                callback(event)


EVENT_BUS = EventBus()
