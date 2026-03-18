from unittest.mock import MagicMock

from engine import InputStateEnum, KeyInputEnum
from engine.api import InputAPI


def test_api_handles_missing_manager():
    mock_engine = MagicMock()
    mock_engine.get_manager.return_value = None

    api = InputAPI(mock_engine)
    assert api.is_pressed(KeyInputEnum.UP) is False
    assert api.get_metrics() is None


def test_api_checks_manager_state():
    mock_engine = MagicMock()
    mock_manager = MagicMock()
    mock_manager._key_states = {KeyInputEnum.UP: InputStateEnum.PRESSED}
    mock_engine.get_manager.return_value = mock_manager

    api = InputAPI(mock_engine)
    assert api.is_pressed(KeyInputEnum.UP) is True
    assert api.is_pressed(KeyInputEnum.DOWN) is False
