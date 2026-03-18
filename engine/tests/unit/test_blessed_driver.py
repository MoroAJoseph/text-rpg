from unittest.mock import MagicMock
from engine import KeyInputEnum
from engine.drivers.blessed import BlessedInputDriver


def test_blessed_driver_special_key():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_key = MagicMock()
    mock_key.name = "KEY_UP"
    mock_term.inkey.return_value = mock_key

    events = driver.poll()
    assert events[0].key == KeyInputEnum.UP
    assert events[0].raw_data == "KEY_UP"


def test_blessed_driver_normal_char():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_key = MagicMock()
    mock_key.name = None
    mock_key.configure_mock(**{"__str__.return_value": " "})
    mock_term.inkey.return_value = mock_key

    events = driver.poll()
    assert events[0].key == KeyInputEnum.SPACE


class FakeKeystroke:
    def __init__(self, name=None, char=" "):
        self.name = name
        self.char = char

    def __str__(self):
        return self.char


def test_blessed_driver_with_fake_object():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)
    mock_term.inkey.return_value = FakeKeystroke(name=None, char=" ")

    events = driver.poll()
    assert events[0].key == KeyInputEnum.SPACE
