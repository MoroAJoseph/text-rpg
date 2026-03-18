from typing import List, TYPE_CHECKING
from ..common.enums import ConnectionCapability
from .system import SystemAPI
from .events import EventsAPI
from .input import InputAPI

if TYPE_CHECKING:
    from ..core.kernel import Engine


class EngineAPI:
    """A dynamic container for requested API handles."""

    if TYPE_CHECKING:
        system: "SystemAPI"
        events: "EventsAPI"
        input: "InputAPI"

    # We leave __init__ empty; attributes are added via setattr
    def __init__(self):
        pass


def connect(engine: "Engine", capabilities: List[ConnectionCapability]) -> EngineAPI:
    """
    Wires specific API handles to an instanced engine.

    :param engine: The Engine instance to connect to.
    :param capabilities: List of ConnectionCapability enums.
    """
    api = EngineAPI()

    mapping = {
        ConnectionCapability.SYSTEM: ("system", SystemAPI),
        ConnectionCapability.EVENTS: ("events", EventsAPI),
        ConnectionCapability.INPUT: ("input", InputAPI),
    }

    for req in capabilities:
        if req in mapping:
            attr_name, api_class = mapping[req]
            # Injecting the engine instance here
            setattr(api, attr_name, api_class(engine))

    return api
