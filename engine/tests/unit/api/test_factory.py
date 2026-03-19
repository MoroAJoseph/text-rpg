from unittest.mock import MagicMock
from engine.api.factory import connect
from engine.domains.input.manager import InputManager


def test_connect_assembles_full_stack():
    engine = MagicMock()
    engine.config.input.enabled = True

    # Mock registry behavior
    mock_input_mgr = MagicMock(spec=InputManager)
    engine.managers.get.return_value = mock_input_mgr

    stack = connect(engine)

    assert stack.events is not None
    assert stack.system is not None
    assert stack.input is not None  # Should be populated
