from typing import TYPE_CHECKING

from ..core import EngineOptions
from ..domains.input import InputManager
from .dataclasses import APIStack
from .system import SystemAPI
from .events import EventsAPI
from .input import InputAPI

if TYPE_CHECKING:
    from ..core import Engine


def create_engine(options: EngineOptions = EngineOptions()) -> "Engine":
    """
    Factory to produce a fresh Engine instance.
    The Engine constructor handles the domain bootstrapping internally.
    """

    from ..core.engine import Engine

    return Engine(options)


def connect(engine: "Engine") -> APIStack:
    """Automated API assembly based on Engine configuration."""
    # 1. Initialize core APIs available to everyone
    api_stack = APIStack(events=EventsAPI(engine), system=SystemAPI(engine))

    # 2. Resolve Input API if enabled
    if engine.options.input.enabled:
        # Late import to prevent circularity between API and Domains
        from ..domains.input.manager import InputManager

        manager = engine.get_manager("input", InputManager)
        if manager:
            api_stack.input = InputAPI(manager)

    return api_stack
