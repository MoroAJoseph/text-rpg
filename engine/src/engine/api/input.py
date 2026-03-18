from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.kernel import Engine


class InputAPI:
    """Interface for querying input state."""

    def __init__(self, engine: "Engine"):
        self._ctx = engine.ctx

    def is_pressed(self, key_name: str) -> bool:
        """Polls the current state from the engine's context."""
        # Logic will check the specific engine instance's input registry
        return False
