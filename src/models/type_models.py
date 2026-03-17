from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypeVar


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


# Game-related enums
class ExitCodeEnum(Enum):
    """Standard exit codes for script/game termination.

    :cvar SUCCESS:
    :cvar GENERAL_ERROR:
    :cvar CLI_ERROR:
    :cvar CANNOT_EXECUTE:
    :cvar COMMAND_NOT_FOUND:
    :cvar TERMINATED_BY_USER:
    :cvar TERMINATED:
    :cvar OUT_OF_RANGE:
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
    """Represents the current state of the game loop.

    :cvar BOOT:
    :cvar MAIN:
    :cvar EXIT:
    """

    BOOT = auto()
    MAIN = auto()
    EXIT = auto()


# UI-related enums
class UIScreensEnum(Enum):
    """Identifiers for full-screen contexts.

    :cvar BOOT:
    :cvar TITLE:
    :cvar GAME:
    """

    BOOT = auto()
    TITLE = auto()
    GAME = auto()


class UIMenusEnum(Enum):
    """Identifiers for overlay menus.

    :cvar MAIN:
    :cvar LOAD_GAME:
    :cvar PAUSE:
    :cvar SETTINGS:
    :cvar WELCOME:
    """

    MAIN = auto()
    LOAD_GAME = auto()
    PAUSE = auto()
    SETTINGS = auto()
    WELCOME = auto()


class UINotificationsEnum(Enum):
    """Identifiers for transient UI notifications."""

    pass


# Event-related enums
class EventTypeEnum(Enum):
    """High-level categories for events.

    :cvar GAME:
    :cvar UI:
    :cvar INPUT:
    :cvar SYSTEM:
    """

    GAME = auto()
    UI = auto()
    INPUT = auto()
    SYSTEM = auto()


class GameEventsEnum(Enum):
    """Game-specific event identifiers.

    :cvar START_GAME:
    :cvar LOAD_GAME:
    :cvar SAVE_GAME:
    :cvar EXIT_GAME:
    """

    START_GAME = auto()
    LOAD_GAME = auto()
    SAVE_GAME = auto()
    EXIT_GAME = auto()


class UIEventsEnum(Enum):
    """UI-specific event identifiers.

    :cvar RENDER:
    :cvar CHANGE_SCREEN:
    :cvar CHANGE_MENU:
    :cvar CLOSE_MENU:
    """

    RENDER = auto()
    CHANGE_SCREEN = auto()
    CHANGE_MENU = auto()
    CLOSE_MENU = auto()


class InputEventsEnum(Enum):
    """Raw input events from the input system.

    - Keys
    :cvar KEY_ARROW_UP:
    :cvar KEY_ARROW_DOWN:
    :cvar KEY_ARROW_LEFT:
    :cvar KEY_ARROW_RIGHT:
    :cvar KEY_ENTER:
    :cvar KEY_BACKSPACE:
    :cvar KEY_ESCAPE:
    :cvar KEY_ANY: Fallback for any other Key events

    - Mouse Button
    :cvar MB_1:
    :cvar MB_2:
    :cvar MB_3:
    :cvar MB_4:
    :cvar MB_5:
    :cvar MB_ANY: Fallback for any other Mouse Button events

    - Mouse Scroll
    :cvar SCROLL_UP:
    :cvar SCROLL_DOWN:
    :cvar SCROLL_ANY: Fallback for any other Scroll event
    """

    # --- Keys ---
    KEY_ARROW_UP = auto()
    KEY_ARROW_DOWN = auto()
    KEY_ARROW_LEFT = auto()
    KEY_ARROW_RIGHT = auto()

    KEY_ENTER = auto()
    KEY_BACKSPACE = auto()

    KEY_M = auto()
    KEY_ESCAPE = auto()
    KEY_ANY = auto()

    # --- Mouse Button ---
    MB_1 = auto()
    MB_2 = auto()
    MB_3 = auto()
    MB_4 = auto()
    MB_5 = auto()
    MB_ANY = auto()

    # --- Scroll ---
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()
    SCROLL_ANY = auto()


class SystemEventsEnum(Enum):
    """System-level events.

    :cvar EXIT:
    """

    EXIT = auto()


class UIActionsEnum(Enum):
    NAV_UP = auto()
    NAV_DOWN = auto()
    NAV_LEFT = auto()
    NAV_RIGHT = auto()
    SELECT = auto()
    BACK = auto()


# Serialized data enums
class GearSlotEnum(StrEnum):
    """Inventory gear slot identifiers for items.

    :cvar WEAPON: Weapon slot
    :cvar HEAD: Headgear slot
    :cvar CHEST: Chest armor slot
    :cvar RING: Ring slot
    :cvar NECK: Necklace slot
    """

    WEAPON = auto()
    HEAD = auto()
    CHEST = auto()
    RING = auto()
    NECK = auto()


# ---
# --- Dataclasses
# ---

EventNameT = TypeVar("EventNameT", bound=Enum)
EventDataT = TypeVar("EventDataT")


@dataclass
class Event(Generic[EventNameT, EventDataT]):
    """Represents a generic event to dispatch through the event manager.

    Attributes:
        type: High-level event category (EventTypeEnum)
        name: Specific event identifier (GameEventsEnum, UIEventsEnum, etc.)
        data: Optional data payload associated with the event
    """

    type: EventTypeEnum
    name: EventNameT
    data: EventDataT | None = None


@dataclass
class ExitRequest:
    """Represents a request to exit the game.

    Attributes:
        code: ExitCodeEnum value indicating the reason for exit
        message: Human-readable message describing the exit
    """

    code: ExitCodeEnum
    message: str
