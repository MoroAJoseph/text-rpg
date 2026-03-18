# The Public Substrate
from .core import (
    Engine,
    CTX,
    Context,
    DomainManager,
    Clock,
    EventTypeEnum,
    SystemEventEnum,
    EngineOptions,
    InputOptions,
    EventData,
)

# The Execution Factory
from .api import create_engine, connect, APIStack, EventsAPI, SystemAPI, InputAPI

# The Feature Domains (Expose only what is needed for type hinting or custom drivers)
from .domains.input import (
    KeyInputEnum,
    InputEvent,
    InputStateEnum,
    InputEventEnum,
    InputManager,
    BlessedInputDriver,
)

__all__ = [
    # Core
    "Engine",
    "CTX",
    "Context",
    "DomainManager",
    "Clock",
    "EventTypeEnum",
    "SystemEventEnum",
    "EngineOptions",
    "InputOptions",
    "EventData",
    # API
    "create_engine",
    "connect",
    "APIStack",
    "EventsAPI",
    "SystemAPI",
    "InputAPI",
    # Input
    "KeyInputEnum",
    "InputEvent",
    "InputStateEnum",
    "InputEventEnum",
    "InputManager",
    "InputOptions",
    "BlessedInputDriver",
]
