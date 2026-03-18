from unittest.mock import MagicMock
from engine import KeyInputEnum
from engine.domains.input import BlessedInputDriver


def test_driver_maps_known_special_keys():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_key = MagicMock()
    mock_key.name = "KEY_ENTER"
    mock_term.inkey.return_value = mock_key

    events = driver.poll()
    # Updated: access via .identifier
    assert events[0].identifier == KeyInputEnum.ENTER


def test_driver_maps_standard_chars():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_key = MagicMock()
    mock_key.name = None
    mock_key.configure_mock(**{"__str__.return_value": " "})
    mock_term.inkey.return_value = mock_key

    events = driver.poll()

    assert len(events) > 0
    assert events[0].identifier == KeyInputEnum.SPACE
    assert events[0].raw_data == " "


def test_driver_returns_default_for_unknown():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_key = MagicMock()
    mock_key.name = "SOME_WEIRD_KEY"
    mock_term.inkey.return_value = mock_key

    events = driver.poll()
    assert events[0].identifier == KeyInputEnum.DEFAULT


class FakeKeystroke:
    def __init__(self, name: str | None = None, char: str = " "):
        self.name = name
        self.char = char

    def __str__(self):
        return self.char


def test_driver_with_stub_object():
    mock_term = MagicMock()
    driver = BlessedInputDriver(mock_term)

    mock_term.inkey.return_value = FakeKeystroke(name=None, char=" ")

    events = driver.poll()
    assert events[0].identifier == KeyInputEnum.SPACE
