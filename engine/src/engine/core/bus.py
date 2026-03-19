from collections import deque
from typing import Callable, Dict, List, Generic, TypeVar, Any
from enum import Enum

from .enums import EventTypeEnum

TName = TypeVar("TName", bound=Enum)
TEvent = TypeVar("TEvent")


class EventBus(Generic[TName, TEvent]):
    """
    A double-buffered substrate for asynchronous event dispatching.
    """

    def __init__(self):
        self._listeners: Dict[TName, List[Callable[[TEvent], Any]]] = {}
        self._type_listeners: Dict[EventTypeEnum, List[Callable[[TEvent], Any]]] = {}
        self._current_queue: deque[TEvent] = deque()
        self._next_queue: deque[TEvent] = deque()

    def subscribe_to_name(self, name: TName, callback: Callable[[TEvent], Any]) -> None:
        """Registers a listener for a specific Enum member (e.g., KEY_UP)."""
        self._listeners.setdefault(name, []).append(callback)

    def subscribe_to_type(
        self, etype: EventTypeEnum, callback: Callable[[TEvent], Any]
    ) -> None:
        """Registers a listener for a broad category (e.g., INPUT)."""
        self._type_listeners.setdefault(etype, []).append(callback)

    def emit(self, event: TEvent) -> None:
        """Queues an event for the next processing cycle."""
        self._next_queue.append(event)

    def process(self) -> None:
        """Swaps buffers and dispatches all queued events to listeners."""
        self._current_queue, self._next_queue = self._next_queue, self._current_queue

        while self._current_queue:
            event = self._current_queue.popleft()

            # Substrate-level attribute lookup
            name = getattr(event, "name", None)
            etype = getattr(event, "type", None)

            # Dispatch to specific name listeners
            if name in self._listeners:
                for cb in self._listeners[name]:
                    cb(event)

            # Dispatch to broad type listeners
            if etype in self._type_listeners:
                for cb in self._type_listeners[etype]:
                    cb(event)
