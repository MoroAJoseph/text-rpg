from enum import Enum, auto


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
# --- Events
# ---


class EventTypeEnum(Enum):
    """Broad categories for the Event Bus to route.

    :cvar SYSTEM: OS-level or application-wide signals.
    :cvar INPUT: Raw hardware input data.
    :cvar UI: UI navigation, rendering, and menu triggers.
    :cvar AUDIO:
    """

    SYSTEM = auto()
    INPUT = auto()
    UI = auto()
    AUDIO = auto()


class SystemEventEnum(Enum):
    """System Event Names for the Event Bus to route.

    :cvar ENGINE_START:
    :cvar ENGINE_STOP:
    :cvar ENGINE_TICK:
    """

    ENGINE_START = auto()
    ENGINE_STOP = auto()
    ENGINE_TICK = auto()
