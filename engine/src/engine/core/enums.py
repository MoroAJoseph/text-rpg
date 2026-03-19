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


# ---
# --- Events
# ---


class EventTypeEnum(Enum):
    """Broad categories for the Event Bus to route.

    :cvar SYSTEM:
    :cvar INPUT:
    """

    SYSTEM = auto()
    INPUT = auto()


class SystemEventEnum(Enum):
    """System Event Names for the Event Bus to route.

    :cvar START:
    :cvar STOP:
    :cvar MAIN_TICK:
    :cvar CUSTOM_TICK:
    """

    START = auto()
    STOP = auto()
    MAIN_TICK = auto()
    CUSTOM_TICK = auto()
