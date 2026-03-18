from collections import defaultdict, deque
from typing import Callable, Dict, List, Generic, TypeVar, Any, Optional
from enum import Enum

TName = TypeVar("TName", bound=Enum)
TEvent = TypeVar("TEvent")


class BaseEventBus(Generic[TName, TEvent]):
    """A generic, double-buffered event system."""

    def __init__(self):
        # We use a standard dict here for better type control during 'get'
        self._listeners: Dict[TName, List[Callable[[TEvent], Any]]] = {}
        self._current_queue: deque[TEvent] = deque()
        self._next_queue: deque[TEvent] = deque()

    def subscribe(self, event_name: TName, callback: Callable[[TEvent], Any]) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def emit(self, event: TEvent) -> None:
        self._next_queue.append(event)

    def _get_event_name(self, event: TEvent) -> Optional[TName]:
        """
        Override this in subclasses to tell the bus how to find
        the Enum name inside your specific TEvent object.
        """
        return getattr(event, "name", None)

    def process(self) -> None:
        self._current_queue, self._next_queue = self._next_queue, self._current_queue

        while self._current_queue:
            event = self._current_queue.popleft()
            name = self._get_event_name(event)

            # Pylance is happy now because we check if name is valid for our dict
            if name is not None and name in self._listeners:
                for callback in self._listeners[name]:
                    callback(event)
