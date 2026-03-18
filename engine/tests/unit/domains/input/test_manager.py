import pytest
from engine import (
    InputEvent,
    InputStateEnum,
    KeyInputEnum,
)
from engine.domains.input import InputManager
from engine.core import EngineEventBus


@pytest.fixture
def manager():
    return InputManager(bus=EngineEventBus())


def test_manager_initial_state(manager):
    assert len(manager._key_states) == 0
    assert len(manager._providers) == 0


def test_process_input_updates_state(manager):
    event = InputEvent(KeyInputEnum.UP, InputStateEnum.PRESSED, 100.0)
    manager._process_input(event)

    assert manager._key_states[KeyInputEnum.UP] == InputStateEnum.PRESSED


def test_duplicate_input_ignored(manager):
    event = InputEvent(KeyInputEnum.UP, InputStateEnum.PRESSED, 100.0)
    manager._process_input(event)

    # Manually clear the bus to see if a second event triggers a new emission
    manager._bus._next_queue.clear()
    manager._process_input(event)

    assert len(manager._bus._next_queue) == 0


def test_handle_key_decay_logic(manager):
    # Setup a pressed key
    key = KeyInputEnum.SPACE
    manager._key_states[key] = InputStateEnum.PRESSED
    manager._key_timers[key] = 0.0

    # Update with dt below threshold (0.12)
    manager._handle_key_decay(0.05)
    assert manager._key_states[key] == InputStateEnum.PRESSED

    # Update to cross threshold
    manager._handle_key_decay(0.08)
    assert manager._key_states[key] == InputStateEnum.RELEASED
    assert key not in manager._key_timers
