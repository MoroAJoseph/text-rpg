from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypeVar, Union, TypeAlias


# ---
# --- Enums
# ---


class StrEnum(str, Enum):
    """
    Base Enum class where values are automatically converted to lowercase strings.
    Useful for serialization and human-readable output.
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


# --- Game ---


class ExitCodeEnum(Enum):
    """Standard exit codes for application termination.

    :cvar SUCCESS: Process finished successfully.
    :cvar GENERAL_ERROR: Catch-all for general errors.
    :cvar CLI_ERROR: Error in command-line arguments or usage.
    :cvar CANNOT_EXECUTE: Command invoked cannot execute.
    :cvar COMMAND_NOT_FOUND: Command or internal routine not found.
    :cvar TERMINATED_BY_USER: User-initiated termination (e.g., Ctrl+C).
    :cvar TERMINATED: System-initiated termination (e.g., SIGTERM).
    :cvar OUT_OF_RANGE: Exit status out of range.
    """

    SUCCESS = auto()
    GENERAL_ERROR = auto()
    CLI_ERROR = auto()
    CANNOT_EXECUTE = auto()
    COMMAND_NOT_FOUND = auto()
    TERMINATED_BY_USER = auto()
    TERMINATED = auto()
    OUT_OF_RANGE = auto()


class GameStateEnum(Enum):
    """High-level states of the game engine lifecycle.

    :cvar BOOT: Initialization and loading phase.
    :cvar MAIN: Active gameplay or menu loop.
    :cvar EXIT: Cleanup and shutdown phase.
    """

    BOOT = auto()
    MAIN = auto()
    EXIT = auto()


# --- UI ---


class UIScreensEnum(Enum):
    """Identifiers for full-screen UI contexts.

    :cvar BOOT: The initial splash or loading screen.
    :cvar TITLE: The main title/landing screen.
    :cvar GAME: The primary gameplay interface.
    """

    BOOT = auto()
    TITLE = auto()
    GAME = auto()


class UIMenusEnum(Enum):
    """Identifiers for interactive overlay menus.

    :cvar MAIN: The primary menu (New Game, Load, Exit).
    :cvar LOAD_GAME: Save-file selection interface.
    :cvar PAUSE: In-game pause overlay.
    :cvar SETTINGS: Configuration and options interface.
    :cvar WELCOME: Initial greeting or tutorial overlay.
    """

    MAIN = auto()
    LOAD_GAME = auto()
    PAUSE = auto()
    SETTINGS = auto()
    WELCOME = auto()


class UIActionsEnum(Enum):
    """Abstracted UI intents mapped from various input types.

    :cvar NAV_UP: Move selection focus upward.
    :cvar NAV_DOWN: Move selection focus downward.
    :var NAV_LEFT: Move selection focus left.
    :cvar NAV_RIGHT: Move selection focus right.
    :cvar SELECT: Confirm or activate the current selection.
    :cvar BACK: Return to the previous screen or close menu.
    """

    NAV_UP = auto()
    NAV_DOWN = auto()
    NAV_LEFT = auto()
    NAV_RIGHT = auto()
    SELECT = auto()
    BACK = auto()


class UINotificationsEnum(Enum):
    """Identifiers for transient notification types."""

    pass


# --- Event ---


class EventTypeEnum(Enum):
    """Broad categories for the Event Bus to route.

    :cvar GAME: High-level game logic and state changes.
    :cvar UI: UI navigation, rendering, and menu triggers.
    :cvar INPUT: Raw hardware input data.
    :cvar SYSTEM: OS-level or application-wide signals.
    """

    GAME = auto()
    UI = auto()
    INPUT = auto()
    SYSTEM = auto()


class GameEventsEnum(Enum):
    """Specific event names for game-logic triggers.

    :cvar START_GAME: Trigger the transition into a new game session.
    :cvar LOAD_GAME: Request loading state from a save file.
    :cvar SAVE_GAME: Request current state persistence.
    :cvar EXIT_GAME: Request the game to initiate shutdown.
    """

    START_GAME = auto()
    LOAD_GAME = auto()
    SAVE_GAME = auto()
    EXIT_GAME = auto()


class UIEventsEnum(Enum):
    """Specific event names for UI system triggers.

    :cvar RENDER: Force a full UI buffer refresh and terminal write.
    :cvar CHANGE_SCREEN: Switch the current base screen.
    :cvar CHANGE_MENU: Push a new menu overlay onto the stack.
    :cvar CLOSE_MENU: Pop the top-most menu overlay from the stack.
    """

    RENDER = auto()
    CHANGE_SCREEN = auto()
    CHANGE_MENU = auto()
    CLOSE_MENU = auto()


class SystemEventsEnum(Enum):
    """Specific event names for system-level triggers.

    :cvar EXIT: Application-wide termination signal.
    """

    EXIT = auto()


# --- Input ---


class KeyInputEnum(Enum):
    """Identifiers for supported keyboard keys.

    :cvar UP: The Up arrow key.
    :cvar DOWN: The Down arrow key.
    :cvar LEFT: The Left arrow key.
    :cvar RIGHT: The Right arrow key.
    :cvar ENTER: The Enter/Return key.
    :cvar BACKSPACE: The Backspace key.
    :cvar ESCAPE: The Escape key.
    :cvar ANY: Generic fallback for unmapped keys.
    """

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    BACKSPACE = auto()
    ESCAPE = auto()
    ANY = auto()


class MouseInputEnum(Enum):
    """Identifiers for mouse buttons.

    :cvar LEFT: Primary mouse button (Button 1).
    :cvar RIGHT: Secondary mouse button (Button 2).
    :cvar MIDDLE: Scroll wheel button (Button 3).
    :cvar MB_4: Auxiliary side button 1.
    :cvar MB_5: Auxiliary side button 2.
    :cvar ANY: Generic fallback for unmapped mouse buttons.
    """

    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()
    MB_4 = auto()
    MB_5 = auto()
    ANY = auto()


class ScrollInputEnum(Enum):
    """Identifiers for mouse wheel scroll directions.

    :cvar UP: Scroll wheel moved upward.
    :cvar DOWN: Scroll wheel moved downward.
    :cvar ANY: Fallback for non-standard scroll inputs.
    """

    UP = auto()
    DOWN = auto()
    ANY = auto()


class InputStateEnum(Enum):
    """The physical state or action of an input device.

    :cvar UP: Key or button was released.
    :cvar DOWN: Key or button was pressed.
    :cvar HELD: Key or button is being held down.
    :cvar MOVE: Mouse cursor moved (for hover logic).
    """

    UP = auto()
    DOWN = auto()
    HELD = auto()
    MOVE = auto()


# Type alias for any input identifier
InputEnum: TypeAlias = Union[KeyInputEnum, MouseInputEnum, ScrollInputEnum]


# --- Serialized ---


class GearSlotEnum(StrEnum):
    """Inventory slots available for equipment.

    :cvar WEAPON: Weapon slot.
    :cvar HEAD: Headgear slot.
    :cvar CHEST: Chest armor slot.
    :cvar RING: Ring slot.
    :cvar NECK: Necklace slot.
    """

    WEAPON = auto()
    HEAD = auto()
    CHEST = auto()
    RING = auto()
    NECK = auto()


# ---
# --- Dataclasses
# ---


# --- Events ---


EventNameT = TypeVar("EventNameT", bound=Enum)
EventDataT = TypeVar("EventDataT")


@dataclass
class Event(Generic[EventNameT, EventDataT]):
    """Represents a generic event to dispatch through the event manager.

    :param type: High-level event category (EventTypeEnum).
    :param name: Specific event identifier (GameEventsEnum, UIEventsEnum, etc.).
    :param data: Optional data payload associated with the event.
    """

    type: EventTypeEnum
    name: EventNameT
    data: EventDataT | None = None


@dataclass
class ExitRequest:
    """Represents a request to exit the game.

    :param code: ExitCodeEnum value indicating the reason for exit.
    :param message: Human-readable message describing the exit.
    """

    code: ExitCodeEnum
    message: str


# --- Input ---


@dataclass
class InputEvent:
    """Base class for all processed hardware input interactions.

    :param state: The current InputStateEnum (DOWN, UP, HELD, MOVE).
    """

    state: InputStateEnum


@dataclass
class KeyInputEvent(InputEvent):
    """A keyboard-specific input event.

    :param key: The KeyInputEnum identifier.
    :param char: The actual string character pressed (if applicable).
    :param is_special: True if it's a non-character key like ARROW_UP.
    """

    key: KeyInputEnum
    char: str | None = None
    is_special: bool = False


@dataclass
class MouseInputEvent(InputEvent):
    """A mouse-specific input event.

    :param button: The button pressed or scroll direction (None if only moving).
    :param x: The horizontal terminal coordinate (1-based).
    :param y: The vertical terminal coordinate (1-based).
    """

    button: Union[MouseInputEnum, ScrollInputEnum, None]
    x: int
    y: int
