from unittest.mock import MagicMock
from engine.domains.input.drivers.blessed import BlessedInputDriver
from engine.domains.input.enums import KeyInputEnum, MouseInputEnum


def test_blessed_keyboard_mapping():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    # Mock a special key
    key = MagicMock()
    key.is_sequence = True
    key.name = "KEY_UP"
    mock_term.inkey.return_value = key

    payloads = driver.poll()
    assert payloads[0].identifier == KeyInputEnum.UP


def test_blessed_mouse_mapping():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    key = MagicMock()
    key.name = "KEY_MOUSE"
    key.button = 0
    key.x, key.y = 10, 20
    mock_term.inkey.return_value = key

    payloads = driver.poll()
    assert payloads[0].identifier == MouseInputEnum.LEFT


def test_blessed_raw_char_mapping():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    # Blessed often returns a raw string for simple keys
    mock_term.inkey.return_value = "a"

    payloads = driver.poll()
    assert payloads[0].identifier == KeyInputEnum.CHAR
    assert payloads[0].raw_data == "a"
