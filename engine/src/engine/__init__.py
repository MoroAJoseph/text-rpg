# The Public Substrate
from .core import (
    Engine,
    CTX,
    Context,
    DomainManager,
    ConnectionCapability,
    Clock,
    EventTypeEnum,
    SystemEventEnum,
    EngineOptions,
    EventData,
)

# The Execution Factory
from .api import create_engine, connect, EngineAPI, EventsAPI, SystemAPI, InputAPI

# The Feature Domains (Expose only what is needed for type hinting or custom drivers)
from .domains.input import (
    KeyInputEnum,
    InputEvent,
    InputStateEnum,
    InputEventEnum,
    BlessedInputDriver,
)

__all__ = [
    # Core
    "Engine",
    "CTX",
    "Context",
    "DomainManager",
    "ConnectionCapability",
    "Clock",
    "EventTypeEnum",
    "SystemEventEnum",
    "EngineOptions",
    "EventData",
    # API
    "create_engine",
    "connect",
    "EngineAPI",
    "EventsAPI",
    "SystemAPI",
    "InputAPI",
    # Input
    "KeyInputEnum",
    "InputEvent",
    "InputStateEnum",
    "InputEventEnum",
    "BlessedInputDriver",
]
