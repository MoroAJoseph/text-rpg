from enum import Enum, auto


class KeyInputEnum(Enum):
    # --- Navigation ---
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    HOME = auto()
    END = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()

    # --- System / Action ---
    ENTER = auto()
    BACKSPACE = auto()
    ESCAPE = auto()
    SPACE = auto()
    TAB = auto()
    INSERT = auto()
    DELETE = auto()
    PRINT_SCREEN = auto()
    SCROLL_LOCK = auto()
    PAUSE = auto()

    # --- Modifiers ---
    LSHIFT = auto()
    RSHIFT = auto()
    LCTRL = auto()
    RCTRL = auto()
    LALT = auto()
    RALT = auto()
    LSUPER = auto()  # Windows/Command Key
    RSUPER = auto()
    CAPS_LOCK = auto()
    NUM_LOCK = auto()

    # --- Function Keys ---
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    F13 = auto()
    F14 = auto()
    F15 = auto()
    F16 = auto()

    # --- Generic Alpha-Numeric ---
    CHAR = auto()  # Any printable character (a-z, 0-9, symbols)

    # --- Numpad ---
    NUM_0 = auto()
    NUM_1 = auto()
    NUM_2 = auto()
    NUM_3 = auto()
    NUM_4 = auto()
    NUM_5 = auto()
    NUM_6 = auto()
    NUM_7 = auto()
    NUM_8 = auto()
    NUM_9 = auto()
    NUM_DECIMAL = auto()
    NUM_DIVIDE = auto()
    NUM_MULTIPLY = auto()
    NUM_SUBTRACT = auto()
    NUM_ADD = auto()
    NUM_ENTER = auto()

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


class InputEventNameEnum(Enum):
    """Categorization for input-related bus traffic.

    :cvar KEYBOARD:
    :cvar MOUSE:
    :cvar SCROLL:
    :cvar CONTROLLER:
    :cvar TELEMETRY:
    """

    KEYBOARD = auto()
    MOUSE = auto()
    SCROLL = auto()
    CONTROLLER = auto()
    TELEMETRY = auto()
