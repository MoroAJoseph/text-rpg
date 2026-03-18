from enum import Enum, auto
from typing import Union


class StrEnum(str, Enum):
    """
    Base Enum class where values are automatically converted to lowercase strings.
    Useful for serialization and human-readable output.
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


# ---
# --- System
# ---


class ExitCodeEnum(Enum):
    """Standard exit codes for application termination.

    :cvar SUCCESS: Process finished successfully.
    :cvar ERROR: Catch-all for general errors.
    :cvar USER_QUIT: User-initiated termination (e.g., Ctrl+C).
    """

    SUCCESS = 0
    ERROR = 1
    USER_QUIT = 130


class ConnectionCapability(Enum):
    SYSTEM = auto()
    EVENTS = auto()
    INPUT = auto()
    AUDIO = auto()
    UI = auto()


# ---
# --- Input
# ---


class KeyInputEnum(Enum):
    """Identifiers for supported keyboard keys.

    :cvar UP: The Up arrow key.
    :cvar DOWN: The Down arrow key.
    :cvar LEFT: The Left arrow key.
    :cvar RIGHT: The Right arrow key.
    :cvar ENTER: The Enter/Return key.
    :cvar BACKSPACE: The Backspace key.
    :cvar ESCAPE: The Escape key.
    :cvar DEFAULT: Generic fallback for unmapped keys.
    """

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    BACKSPACE = auto()
    ESCAPE = auto()
    SPACE = auto()
    DEFAULT = auto()


class MouseInputEnum(Enum):
    """Identifiers for mouse buttons.

    :cvar LEFT: Primary mouse button (Button 1).
    :cvar RIGHT: Secondary mouse button (Button 2).
    :cvar MIDDLE: Scroll wheel button (Button 3).
    :cvar MB_4: Auxiliary side button 1.
    :cvar MB_5: Auxiliary side button 2.
    :cvar DEFAULT: Generic fallback for unmapped mouse buttons.
    """

    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()
    MB_4 = auto()
    MB_5 = auto()
    DEFAULT = auto()


class ScrollInputEnum(Enum):
    """Identifiers for mouse wheel scroll directions.

    :cvar UP: Scroll wheel moved upward.
    :cvar DOWN: Scroll wheel moved downward.
    :cvar DEFAULT: Fallback for non-standard scroll inputs.
    """

    UP = auto()
    DOWN = auto()
    DEFAULT = auto()


class InputStateEnum(Enum):
    """The physical state or action of an input device.

    :cvar PRESSED: Key or button was pressed.
    :cvar RELEASED: Key or button was released.
    :cvar HELD: Key or button is being held down.
    """

    PRESSED = auto()
    RELEASED = auto()
    HELD = auto()


# ---
# --- Events
# ---


class EventTypeEnum(Enum):
    """Broad categories for the Event Bus to route.

    :cvar SYSTEM: OS-level or application-wide signals.
    :cvar INPUT: Raw hardware input data.
    :cvar UI: UI navigation, rendering, and menu triggers.
    :cvar AUDIO:
    :cvar TELEMETRY: Performance and monitoring data.
    """

    SYSTEM = auto()
    INPUT = auto()
    UI = auto()
    AUDIO = auto()
    TELEMETRY = auto()


class SystemEventEnum(Enum):
    """System Event Names for the Event Bus to route.

    :cvar ENGINE_START:
    :cvar ENGINE_STOP:
    :cvar ENGINE_TICK:
    """

    ENGINE_START = auto()
    ENGINE_STOP = auto()
    ENGINE_TICK = auto()


EventName = Union[
    SystemEventEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
]
