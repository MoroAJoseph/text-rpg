from unittest.mock import MagicMock
from engine.api.input import InputAPI
from engine.domains.input.enums import KeyInputEnum, InputStateEnum


def test_input_api_is_down():
    mock_manager = MagicMock()
    # Mock internal dict state
    mock_manager._key_states = {KeyInputEnum.SPACE: InputStateEnum.HELD}

    api = InputAPI(mock_manager)
    assert api.is_down(KeyInputEnum.SPACE) is True
    assert api.is_down(KeyInputEnum.ESCAPE) is False


def test_input_api_metrics_null_safety():
    mock_manager = MagicMock()
    mock_manager.telemetry = None
    api = InputAPI(mock_manager)
    assert api.get_metrics() is None
