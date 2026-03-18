from collections import deque
from typing import Callable, Dict, List, Generic, TypeVar, Any, Optional
from enum import Enum

from engine.core.enums import EventTypeEnum

TName = TypeVar("TName", bound=Enum)
TEvent = TypeVar("TEvent")


class BaseEventBus(Generic[TName, TEvent]):
    """
    A generic, double-buffered event system designed to prevent
    event-chaining side effects during a single frame update.
    """

    def __init__(self):
        self._listeners: Dict[TName, List[Callable[[TEvent], Any]]] = {}
        self._type_listeners: Dict[EventTypeEnum, List[Callable[[TEvent], Any]]] = {}
        self._current_queue: deque[TEvent] = deque()
        self._next_queue: deque[TEvent] = deque()

    def _get_event_type(self, event: TEvent) -> Optional[EventTypeEnum]:
        """Override in subclass to tell the bus how to find the EventTypeEnum."""
        return getattr(event, "type", None)

    def _get_event_name(self, event: TEvent) -> Optional[TName]:
        """
        Override this in subclasses to tell the bus how to find
        the Enum name inside your specific TEvent object.
        """
        return getattr(event, "name", None)

    def subscribe(self, event_name: TName, callback: Callable[[TEvent], Any]) -> None:
        """
        Registers a callback to be executed when a specific event name is processed.

        Args:
            event_name (TName): The Enum member representing the event subject.
            callback (Callable[[TEvent], Any]): The function to execute.
                Receives the full event object.
        """

        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def subscribe_to_type(
        self, event_type: EventTypeEnum, callback: Callable[[TEvent], Any]
    ) -> None:
        """Registers a listener for a broad category (e.g., INPUT)."""
        if event_type not in self._type_listeners:
            self._type_listeners[event_type] = []
        self._type_listeners[event_type].append(callback)

    def emit(self, event: TEvent) -> None:
        """
        Pushes an event into the 'next' queue. It will not be processed
        until the next call to process().

        Args:
            event (TEvent): The event packet to be queued.
        """

        self._next_queue.append(event)

    def process(self) -> None:
        self._current_queue, self._next_queue = self._next_queue, self._current_queue

        while self._current_queue:
            event: TEvent = self._current_queue.popleft()
            name = self._get_event_name(event)
            etype = self._get_event_type(event)  # Get the category (INPUT, SYSTEM, etc)

            # Listeners
            if name is not None and name in self._listeners:
                for callback in self._listeners[name]:
                    callback(event)

            # Type Listeners
            if etype is not None and etype in self._type_listeners:
                for callback in self._type_listeners[etype]:
                    callback(event)
