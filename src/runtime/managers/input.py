import threading
import time
from blessed import Terminal
from src.models.type_models import (
    Event,
    EventTypeEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
    TelemetryData,
    TelemetryEventsEnum,
)
from ..event_bus import EVENT_BUS
from ..logger import LOGGER

term = Terminal()

# Keyboard mapping
KEY_MAP: dict[str, KeyInputEnum] = {
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

# Mouse mapping
MOUSE_BUTTON_MAP: dict[str, MouseInputEnum] = {
    "BUTTON1": MouseInputEnum.LEFT,
    "BUTTON2": MouseInputEnum.RIGHT,
    "BUTTON3": MouseInputEnum.MIDDLE,
    "BUTTON4": MouseInputEnum.MB_4,
    "BUTTON5": MouseInputEnum.MB_5,
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

        # telemetry state
        self._last_key: str | None = None

        self._initialized = True
        LOGGER.info("InputManager (blessed) initialized.")
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    # --- Main loop ---
    def _run(self):
        with term.cbreak(), term.keypad(), term.hidden_cursor():
            print(term.enable_mouse(), end="", flush=True)

            while not self._stop_event.is_set():
                key = term.inkey(timeout=self.POLL_INTERVAL)
                now = time.perf_counter()

                if not key:
                    continue

                # --- Mouse ---
                if key.name == "KEY_MOUSE":
                    me = term.mouse()
                    if me:
                        self._handle_mouse(me, now)
                    continue

                # --- Keyboard ---
                name = key.name or str(key)
                mapped = KEY_MAP.get(name)

                if mapped:
                    self._emit(mapped, "down", now)
                else:
                    self._emit(KeyInputEnum.ANY, str(key), now)

    # --- Mouse handler ---
    def _handle_mouse(self, me, timestamp: float):
        btn = me.button

        if btn == "SCROLL_UP":
            name = ScrollInputEnum.UP
        elif btn == "SCROLL_DOWN":
            name = ScrollInputEnum.DOWN
        else:
            name = MOUSE_BUTTON_MAP.get(btn, MouseInputEnum.ANY)

        self._emit(name, me.event, timestamp)

    # --- Emit + Telemetry ---
    def _emit(
        self,
        name: KeyInputEnum | MouseInputEnum | ScrollInputEnum,
        data,
        timestamp: float,
    ):
        with self._lock:
            # Emit input event
            EVENT_BUS.emit(
                Event(
                    type=EventTypeEnum.INPUT,
                    name=name,
                    data=data,
                )
            )

            # --- Update last_key ---
            if isinstance(name, KeyInputEnum):
                if isinstance(data, str):
                    self._last_key = data
                else:
                    self._last_key = name.name

            elif isinstance(name, (MouseInputEnum, ScrollInputEnum)):
                self._last_key = name.name

            # --- Latency (ms) ---
            latency_ms = (time.perf_counter() - timestamp) * 1000

            # Emit telemetry
            EVENT_BUS.emit(
                Event(
                    type=EventTypeEnum.TELEMETRY,
                    name=TelemetryEventsEnum.UPDATE,
                    data=TelemetryData(
                        last_key=self._last_key,
                        latency_ms=latency_ms,
                    ),
                )
            )


# Singleton
INPUT_MANAGER = InputManager()

# TODO: Key DOWN events are being emitted TWICE
# TODO: Pass they full InputEvent