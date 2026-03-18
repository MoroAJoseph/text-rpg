from enum import Enum, auto


class KeyInputEnum(Enum):
    """Identifiers for supported keyboard keys.

    :cvar UP: Arrow UP.
    :cvar DOWN: Arrow DOWN.
    :cvar LEFT: Arrow LEFT.
    :cvar RIGHT: Arrow RIGHT.
    :cvar ENTER:
    :cvar BACKSPACE:
    :cvar ESCAPE:
    :cvar SPACE:
    :cvar TAB:
    :cvar HOME:
    :cvar END:
    :cvar PAGE_UP:
    :cvar PAGE_DOWN:
    :cvar INSERT:
    :cvar DELETE:
    :cvar F1:
    :cvar F2:
    :cvar F3:
    :cvar F4:
    :cvar F5:
    :cvar F6:
    :cvar F7:
    :cvar F8:
    :cvar F9:
    :cvar F10:
    :cvar F11:
    :cvar F12:
    :cvar CHAR:
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
    TAB = auto()
    HOME = auto()
    END = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()
    INSERT = auto()
    DELETE = auto()
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
    CHAR = auto()  # For all alpha-numeric characters
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


class InputEventEnum(Enum):
    """Categorization for input-related bus traffic.

    :cvar KEYBOARD:
    :cvar MOUSE:
    :cvar SCROLL:
    :cvar TELEMETRY:
    """

    KEYBOARD = auto()
    MOUSE = auto()
    SCROLL = auto()
    TELEMETRY = auto()
