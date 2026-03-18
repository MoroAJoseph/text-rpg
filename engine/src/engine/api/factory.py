from typing import List, TYPE_CHECKING
from ..core import EngineOptions, ConnectionCapability
from ..domains.input import InputManager
from .system import SystemAPI
from .events import EventsAPI
from .input import InputAPI

if TYPE_CHECKING:
    from ..core import Engine


class EngineAPI:
    """A dynamic container for requested API handles."""

    if TYPE_CHECKING:
        system: "SystemAPI"
        events: "EventsAPI"
        input: "InputAPI"

    # We leave __init__ empty; attributes are added via setattr
    def __init__(self):
        pass


def create_engine(options: EngineOptions = EngineOptions()) -> "Engine":
    """Factory to produce and pre-configure a fresh Engine instance."""
    from ..core.engine import Engine

    engine = Engine(options)

    # Dependency Injection: We wire domains to the kernel here
    if options.use_input:
        # Pass the bus from the engine's context to the manager
        engine.register_manager("input", InputManager(bus=engine.ctx.bus))

    return engine


def connect(engine: "Engine", capabilities: List[ConnectionCapability]) -> EngineAPI:
    """
    Wires specific API handles to an instanced engine.
    Only connects capabilities if the engine has the corresponding manager.
    """
    api = EngineAPI()

    # Mapping: Capability -> (Attribute Name, API Class, Manager Key)
    # Note: System and Events are Core, so they don't need a manager check
    mapping = {
        ConnectionCapability.SYSTEM: ("system", SystemAPI, None),
        ConnectionCapability.EVENTS: ("events", EventsAPI, None),
        ConnectionCapability.INPUT: ("input", InputAPI, "input"),
    }

    for capability in capabilities:
        if capability not in mapping:
            continue

        attr_name, api_class, manager_key = mapping[capability]

        # If it's a domain manager, verify it exists before connecting the API
        if manager_key and manager_key not in engine.managers:
            continue

        setattr(api, attr_name, api_class(engine))

    return api
