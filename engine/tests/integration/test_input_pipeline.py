import time
from unittest.mock import MagicMock
from engine.domains.input.enums import (
    KeyInputEnum,
    InputStateEnum,
    InputEventNameEnum,
    InputEventNameEnum,
)
from engine.domains.input.models import InputPayload
from engine.domains.input.manager import InputManager


def test_keypress_round_trip(test_env):
    engine, api = test_env
    input_manager = engine.managers.get("input", InputManager)

    mock_driver = MagicMock()

    input_manager.add_spoke("mock_kb", mock_driver, 60.0)

    hits = []

    def on_input(event):
        payload: InputPayload = event.data
        if payload.identifier == KeyInputEnum.CHAR:
            hits.append(event)

    api.events.on(InputEventNameEnum.KEYBOARD, on_input)

    # Simulate a PRESSED
    mock_driver.poll.side_effect = [
        [
            InputPayload(
                identifier=KeyInputEnum.CHAR,
                state=InputStateEnum.PRESSED,
                timestamp=time.perf_counter(),
                raw_data="a",
            )
        ],
        [],
        [],
        [],
    ]

    engine.update()  # Tick 1: Poll Release
    engine.update()  # Tick 2: Manager updates bitmask
    engine.update()  # Tick 3: API state settles

    assert len(hits) == 1
    assert api.input.is_down(KeyInputEnum.CHAR) is True

    # Simulate a RELEASE
    mock_driver.poll.side_effect = [
        [
            InputPayload(
                identifier=KeyInputEnum.CHAR,
                state=InputStateEnum.RELEASED,
                timestamp=time.perf_counter(),
                raw_data="a",
            )
        ],
        [],
        [],
    ]

    engine.update()  # Tick 4: Poll Release
    engine.update()  # Tick 5: Manager updates bitmask
    engine.update()  # Tick 6: API state settles

    assert api.input.is_down(KeyInputEnum.CHAR) is False
