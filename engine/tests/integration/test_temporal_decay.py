from unittest.mock import MagicMock, patch

from engine.domains.input.enums import InputStateEnum, KeyInputEnum
from engine.domains.input.manager import InputManager


def test_key_decay_integration(test_env):
    engine, api = test_env
    mgr = engine.managers.get("input", InputManager)

    mgr._key_states[KeyInputEnum.SPACE] = InputStateEnum.PRESSED
    mgr._key_timers[KeyInputEnum.SPACE] = 0.0

    with patch.object(engine.clock, "tick", return_value=0.15):
        engine.update()  # Tick 1: Emits RELEASE to bus _next_queue
        engine.update()  # Tick 2: Bus flushes to API state

    assert api.input.is_down(KeyInputEnum.SPACE) is False
