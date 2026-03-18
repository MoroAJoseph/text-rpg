from typing import TYPE_CHECKING
from ..domains.input import InputManager, InputStateEnum, KeyInputEnum

if TYPE_CHECKING:
    from engine.core.engine import Engine


class InputAPI:
    def __init__(self, engine: "Engine"):
        self._manager: InputManager | None = engine.get_manager("input", InputManager)

    def is_pressed(self, key: KeyInputEnum) -> bool:
        """Instant check for key state."""
        if not self._manager:
            return False
        state = self._manager._key_states.get(key)
        return state == InputStateEnum.PRESSED

    def get_metrics(self):
        """Expose telemetry to the developer."""
        return self._manager.telemetry.metrics if self._manager else None
