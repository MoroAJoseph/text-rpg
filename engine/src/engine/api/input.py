from ..domains.input import InputManager, InputStateEnum, KeyInputEnum


class InputAPI:
    """High-level queries for input state and telemetry."""

    def __init__(self, manager: InputManager):
        self._manager = manager

    def is_down(self, key: KeyInputEnum) -> bool:
        """Returns True if the key is currently PRESSED or HELD."""
        state = self._manager._key_states.get(key)
        return state in (InputStateEnum.PRESSED, InputStateEnum.HELD)

    def get_metrics(self):
        """Access real-time input performance data."""
        return self._manager.telemetry.metrics if self._manager.telemetry else None
