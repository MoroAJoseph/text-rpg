from engine.domains.input.drivers.default import DefaultInputDriver
from engine.domains.input.enums import KeyInputEnum, MouseInputEnum, ScrollInputEnum


def test_ansi_navigation_keys():
    driver = DefaultInputDriver()
    driver._buffer = ["\x1b[A"]  # Raw UP arrow

    payloads = driver.poll()
    assert payloads[0].identifier == KeyInputEnum.UP


def test_sgr_mouse_parsing():
    driver = DefaultInputDriver()
    # SGR Mouse: Button 0 (Left), X=5, Y=10, 'M' (Pressed)
    driver._buffer = ["\x1b[<0;5;10M"]

    payloads = driver.poll()
    assert payloads[0].identifier == MouseInputEnum.LEFT
    assert payloads[0].coords == (5, 10)


def test_sgr_scroll_parsing():
    driver = DefaultInputDriver()
    # SGR Scroll: Button 64 (Scroll Up)
    driver._buffer = ["\x1b[<64;0;0M"]

    payloads = driver.poll()
    assert payloads[0].identifier == ScrollInputEnum.UP


def test_multi_char_chunk():
    driver = DefaultInputDriver()
    # "abc" followed by a UP arrow in one read
    driver._buffer = ["abc\x1b[A"]

    payloads = driver.poll()
    # Does it return 4 payloads? (a, b, c, and UP)
    assert len(payloads) == 4
    assert payloads[3].identifier == KeyInputEnum.UP
