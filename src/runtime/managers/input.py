import threading
from blessed import Terminal
from src.models.type_models import InputEventsEnum, Event, EventTypeEnum
from ..event_bus import EVENT_BUS
from ..logger import LOGGER

term = Terminal()

# Keyboard mapping (terminal → InputEventsEnum)
KEY_MAP = {
    "KEY_UP": InputEventsEnum.KEY_ARROW_UP,
    "KEY_DOWN": InputEventsEnum.KEY_ARROW_DOWN,
    "KEY_LEFT": InputEventsEnum.KEY_ARROW_LEFT,
    "KEY_RIGHT": InputEventsEnum.KEY_ARROW_RIGHT,
    "KEY_ENTER": InputEventsEnum.KEY_ENTER,
    "KEY_ESCAPE": InputEventsEnum.KEY_ESCAPE,
    "\n": InputEventsEnum.KEY_ENTER,
    "\r": InputEventsEnum.KEY_ENTER,
    "KEY_BACKSPACE": InputEventsEnum.KEY_BACKSPACE,
}

# Mouse button mapping
MOUSE_BUTTON_MAP = {
    "BUTTON1": InputEventsEnum.MB_1,
    "BUTTON2": InputEventsEnum.MB_2,
    "BUTTON3": InputEventsEnum.MB_3,
    "BUTTON4": InputEventsEnum.MB_4,
    "BUTTON5": InputEventsEnum.MB_5,
}


class InputManager:
    """Cross-platform terminal input manager using blessed."""

    _instance = None
    _lock = threading.RLock()
    POLL_INTERVAL = 0.01

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
        self._initialized = True
        LOGGER.info("InputManager (blessed) initialized.")
        self._thread.start()

    def stop(self):
        """Stop input thread."""
        self._stop_event.set()
        self._thread.join()

    # --- Main loop ---
    def _run(self):
        with term.cbreak(), term.keypad(), term.hidden_cursor():
            # Enable mouse reporting
            print(term.enable_mouse(), end="", flush=True)

            while not self._stop_event.is_set():
                key = term.inkey(timeout=self.POLL_INTERVAL)
                if not key:
                    continue

                # --- Mouse events ---
                if key.name == "KEY_MOUSE":
                    me = term.mouse()
                    if me:
                        self._handle_mouse(me)
                    continue

                # --- Keyboard events ---
                name = key.name or str(key)
                mapped = KEY_MAP.get(name)
                if mapped:
                    self._emit(mapped, "down")
                else:
                    self._emit(InputEventsEnum.KEY_ANY, str(key))

    # --- Mouse handler ---
    def _handle_mouse(self, me):
        """
        me: blessed.mouse.MouseEvent
        Attributes:
            .event  → 'press', 'release', 'scroll'
            .button → 'BUTTON1', 'BUTTON2', 'SCROLL_UP', 'SCROLL_DOWN', etc.
            .x, .y
        """
        btn = me.button

        # Scroll events
        if btn == "SCROLL_UP":
            name = InputEventsEnum.SCROLL_UP
        elif btn == "SCROLL_DOWN":
            name = InputEventsEnum.SCROLL_DOWN
        else:
            # Map buttons
            name = MOUSE_BUTTON_MAP.get(btn, InputEventsEnum.MB_ANY)

        # Emit mouse input
        self._emit(name, me.event)

    # --- Emit to EventBus ---
    def _emit(self, name: InputEventsEnum, data):
        """Emit event to EventBus."""
        with self._lock:
            EVENT_BUS.emit(Event(type=EventTypeEnum.INPUT, name=name, data=data))
            LOGGER.debug(f"Input event emitted: {name.name} {data}")


# Singleton instance
INPUT_MANAGER = InputManager()
