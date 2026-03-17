import threading
import time
from typing import Dict, Any
from blessed import Terminal
from src.models.type_models import (
    Event,
    EventTypeEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
    InputStateEnum,
    KeyInputEvent,
    MouseInputEvent,
)
from ..event_bus import EVENT_BUS
from ..logger import LOGGER

term = Terminal()

# Keyboard mapping
KEY_MAP = {
    "KEY_UP": KeyInputEnum.UP,
    "KEY_DOWN": KeyInputEnum.DOWN,
    "KEY_LEFT": KeyInputEnum.LEFT,
    "KEY_RIGHT": KeyInputEnum.RIGHT,
    "KEY_ENTER": KeyInputEnum.ENTER,
    "KEY_ESCAPE": KeyInputEnum.ESCAPE,
    "\n": KeyInputEnum.ENTER,
    "\r": KeyInputEnum.ENTER,
    "KEY_BACKSPACE": KeyInputEnum.BACKSPACE,
}

# Mouse button mapping
MOUSE_BUTTON_MAP = {
    "BUTTON1": MouseInputEnum.LEFT,
    "BUTTON2": MouseInputEnum.MIDDLE,
    "BUTTON3": MouseInputEnum.RIGHT,
    "BUTTON4": MouseInputEnum.MB_4,
    "BUTTON5": MouseInputEnum.MB_5,
}


class InputManager:
    """Processes terminal signals into rich KeyInputEvent and MouseInputEvent objects."""

    _instance = None
    _lock = threading.RLock()
    POLL_INTERVAL = 0.005  # Faster polling for lower latency

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

        # State tracking
        self.last_mouse_pos = (-1, -1)
        self.key_states: Dict[KeyInputEnum, float] = {}

        self._initialized = True
        LOGGER.info("InputManager (Rich Events) initialized.")
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _run(self):
        # ENTER_FULLSCREEN and alternate buffer to prevent scrollbars
        print(term.enter_fullscreen + term.hide_cursor, end="", flush=True)

        with term.cbreak(), term.keypad():
            # Enable mouse reporting (SGR mode for better coordinate support)
            print(term.enable_mouse(), end="", flush=True)

            while not self._stop_event.is_set():
                key = term.inkey(timeout=self.POLL_INTERVAL)

                if key.name == "KEY_MOUSE":
                    me = term.mouse()
                    if me:
                        self._handle_mouse(me)
                elif key:
                    self._handle_keyboard(key)

                # Logic for HELD states could be processed here by checking self.key_states

    def _handle_keyboard(self, key):
        name = key.name or str(key)
        mapped_key = KEY_MAP.get(name, KeyInputEnum.ANY)

        is_special = key.is_sequence
        state = InputStateEnum.DOWN

        # Simple repeat detection: if pressed again very quickly, consider it 'HELD'
        now = time.time()
        if mapped_key in self.key_states and (now - self.key_states[mapped_key] < 0.1):
            state = InputStateEnum.HELD

        self.key_states[mapped_key] = now

        event_data = KeyInputEvent(
            state=state,
            key=mapped_key,
            char=str(key) if not is_special else None,
            is_special=is_special,
        )
        self._emit(mapped_key, event_data)

    def _handle_mouse(self, me):
        """
        Processes blessed MouseEvent into MouseInputEvent.
        Supports MOVE (hover), DOWN/UP (clicks), and SCROLL.
        """
        # Coordinate tracking for MOVE state
        current_pos = (me.x, me.y)
        if current_pos != self.last_mouse_pos:
            self.last_mouse_pos = current_pos
            # If the event is just movement, emit a MOVE event
            if me.event == "move":
                self._emit(
                    MouseInputEnum.ANY,
                    MouseInputEvent(
                        state=InputStateEnum.MOVE, button=None, x=me.x, y=me.y
                    ),
                )
                return

        # Button Mapping
        button = None
        state = InputStateEnum.DOWN if me.event == "press" else InputStateEnum.UP

        if me.button == "SCROLL_UP":
            button = ScrollInputEnum.UP
        elif me.button == "SCROLL_DOWN":
            button = ScrollInputEnum.DOWN
        else:
            button = MOUSE_BUTTON_MAP.get(me.button, MouseInputEnum.ANY)

        event_data = MouseInputEvent(state=state, button=button, x=me.x, y=me.y)
        self._emit(button or MouseInputEnum.ANY, event_data)

    def _emit(self, name: Any, data: Any):
        with self._lock:
            EVENT_BUS.emit(Event(type=EventTypeEnum.INPUT, name=name, data=data))


# Singleton instance
INPUT_MANAGER = InputManager()
