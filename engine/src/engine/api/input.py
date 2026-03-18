from ..domains.input import InputManager, InputStateEnum, KeyInputEnum


class InputAPI:
    def __init__(self, manager: InputManager):
        self._manager: InputManager = manager

    def is_pressed(self, key: KeyInputEnum) -> bool:
        """Instant check for key state."""
        if not self._manager:
            return False
        state = self._manager._key_states.get(key)
        return state == InputStateEnum.PRESSED

    def get_metrics(self):
        """Expose telemetry to the developer."""
        return self._manager.telemetry.metrics if self._manager else None
