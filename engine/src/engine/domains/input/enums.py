from enum import Enum, auto


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
