from typing import TYPE_CHECKING
from .models import APIStack
from .system import SystemAPI
from .events import EventsAPI
from .input import InputAPI

if TYPE_CHECKING:
    from ..kernel import Engine


def connect(engine: "Engine") -> APIStack:
    """Assembles the APIStack based on engine configuration."""
    # Core APIs
    stack = APIStack(events=EventsAPI(engine), system=SystemAPI(engine))

    # Conditional Input API
    if engine.config.input.enabled:
        from ..domains.input.manager import InputManager

        # ManagerRegistry.get provides type-safe retrieval
        manager = engine.managers.get("input", InputManager)
        if manager:
            stack.input = InputAPI(manager)

    return stack
