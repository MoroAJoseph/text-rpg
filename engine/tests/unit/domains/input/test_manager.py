import pytest
from unittest.mock import MagicMock
from engine.domains.input.manager import InputManager
from engine.domains.input.models import InputPayload
from engine.domains.input.enums import KeyInputEnum, InputStateEnum, InputEventNameEnum
from engine.config.models import InputConfig
from engine.core.bus import EventBus


@pytest.fixture
def manager():
    config = InputConfig(decay_threshold=0.1)
    m = InputManager(config)
    m.register_bus(EventBus())
    return m


def test_promotion_pressed_to_held(manager):
    payload = InputPayload(
        identifier=KeyInputEnum.SPACE,
        state=InputStateEnum.PRESSED,
        timestamp=1.0,
        raw_data=" ",
    )

    # First press
    manager._process_input(payload)
    assert manager._key_states[KeyInputEnum.SPACE] == InputStateEnum.PRESSED

    # Second press (same key) -> Promotion to HELD
    manager._process_input(payload)
    assert manager._key_states[KeyInputEnum.SPACE] == InputStateEnum.HELD


def test_key_decay_to_released(manager):
    key = KeyInputEnum.ENTER
    manager._key_states[key] = InputStateEnum.PRESSED
    manager._key_timers[key] = 0.0

    # Step time forward by 0.11 (threshold is 0.1)
    manager._handle_key_decay(0.11)

    assert manager._key_states[key] == InputStateEnum.RELEASED
    assert key not in manager._key_timers  # Cleanup check


def test_spoke_polling_logic(manager):
    mock_driver = MagicMock()

    # Use keywords to ensure 'a' goes to raw_data, not coords
    mock_driver.poll.return_value = [
        InputPayload(
            identifier=KeyInputEnum.CHAR,
            state=InputStateEnum.PRESSED,
            timestamp=1.0,
            raw_data="a",
        )
    ]

    # Add spoke at 60Hz
    manager.add_spoke("test_kb", mock_driver, 60.0)

    # Update manager with enough dt (0.02s) to exceed 60Hz interval (~0.016s)
    manager.update(0.02)

    assert manager._key_states[KeyInputEnum.CHAR] == InputStateEnum.PRESSED
    mock_driver.poll.assert_called_once()
