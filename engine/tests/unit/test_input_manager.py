from unittest.mock import MagicMock
from engine import KeyInputEnum, InputStateEnum, InputEvent
from engine.managers.input import InputManager
from engine.core.event_bus import EngineEventBus


def test_input_manager_ignores_duplicate_states():
    # Injecting a local bus to avoid global state
    bus = EngineEventBus()
    manager = InputManager(bus=bus)

    mock_provider = MagicMock()
    duplicate_events = [
        InputEvent(key=KeyInputEnum.UP, state=InputStateEnum.PRESSED, timestamp=1.0),
        InputEvent(key=KeyInputEnum.UP, state=InputStateEnum.PRESSED, timestamp=1.1),
    ]
    mock_provider.poll.return_value = duplicate_events
    manager.register_provider(mock_provider)

    manager.update()

    assert manager._key_states[KeyInputEnum.UP] == InputStateEnum.PRESSED
    # The internal bus should have exactly 1 event queued
    assert len(bus._next_queue) == 1
