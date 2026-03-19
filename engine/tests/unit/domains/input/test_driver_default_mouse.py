import pytest
from engine.domains.input.drivers.default import DefaultInputDriver
from engine.domains.input.enums import MouseInputEnum, ScrollInputEnum, InputStateEnum

# --- EXTERNAL MOUSE TRUTH TABLE ---
# Format: (SGR_Sequence, Expected_Enum, Expected_State, Expected_Coords)
MOUSE_SPEC = [
    # --- LEFT BUTTON ---
    ("\x1b[<0;1;1M", MouseInputEnum.LEFT, InputStateEnum.PRESSED, (1, 1)),
    ("\x1b[<0;80;24m", MouseInputEnum.LEFT, InputStateEnum.RELEASED, (80, 24)),
    # --- MIDDLE BUTTON ---
    ("\x1b[<1;10;10M", MouseInputEnum.MIDDLE, InputStateEnum.PRESSED, (10, 10)),
    ("\x1b[<1;10;10m", MouseInputEnum.MIDDLE, InputStateEnum.RELEASED, (10, 10)),
    # --- RIGHT BUTTON ---
    ("\x1b[<2;50;5M", MouseInputEnum.RIGHT, InputStateEnum.PRESSED, (50, 5)),
    ("\x1b[<2;50;5m", MouseInputEnum.RIGHT, InputStateEnum.RELEASED, (50, 5)),
    # --- SCROLL WHEEL ---
    # Note: Scroll events are typically stateless "Presses" in terminal emulators
    ("\x1b[<64;0;0M", ScrollInputEnum.UP, InputStateEnum.PRESSED, (0, 0)),
    ("\x1b[<65;0;0M", ScrollInputEnum.DOWN, InputStateEnum.PRESSED, (0, 0)),
    # --- HIGH COORDINATE TEST (Beyond 223) ---
    # SGR 1006 was specifically designed to fix coordinate limits
    ("\x1b[<0;500;500M", MouseInputEnum.LEFT, InputStateEnum.PRESSED, (500, 500)),
]


@pytest.mark.parametrize("raw, identifier, state, coords", MOUSE_SPEC)
def test_mouse_parsing_completeness(raw, identifier, state, coords):
    """Verifies all mouse buttons, states, and coordinate ranges."""
    driver = DefaultInputDriver()
    driver._buffer = [raw]

    payloads = driver.poll()

    assert len(payloads) == 1
    payload = payloads[0]

    assert payload.identifier == identifier
    assert payload.state == state
    assert payload.coords == coords
    assert payload.raw_data == raw


def test_mouse_mixed_with_keyboard():
    """Verifies that mouse sequences don't break the lexer when followed by keys."""
    driver = DefaultInputDriver()
    # Scenario: Click at (1,1) then immediately press 'q'
    stream = "\x1b[<0;1;1Mq"
    driver._buffer = [stream]

    payloads = driver.poll()

    assert len(payloads) == 2
    assert payloads[0].identifier == MouseInputEnum.LEFT
    assert payloads[0].coords == (1, 1)

    from engine.domains.input.enums import KeyInputEnum

    assert payloads[1].identifier == KeyInputEnum.CHAR
    assert payloads[1].raw_data == "q"


def test_malformed_mouse_sequence():
    """Verifies that an incomplete mouse sequence falls back safely."""
    driver = DefaultInputDriver()
    # Missing the trailing 'M' or 'm'
    driver._buffer = ["\x1b[<0;1;1"]

    payloads = driver.poll()

    # It should not recognize it as a mouse event and treat it as raw escape + chars
    assert payloads[0].identifier != MouseInputEnum.LEFT
