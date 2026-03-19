import pytest
from engine.domains.input.drivers.default import DefaultInputDriver
from engine.domains.input.enums import KeyInputEnum

# --- EXTERNAL TRUTH TABLE (THE TEST SPEC) ---
# This is our source of truth for every key on a standard keyboard.
FULL_KEYBOARD_SPEC = [
    # --- CONTROL & WHITESPACE ---
    ("\r", KeyInputEnum.ENTER),
    ("\n", KeyInputEnum.ENTER),
    ("\t", KeyInputEnum.TAB),
    ("\x1b", KeyInputEnum.ESCAPE),
    ("\x7f", KeyInputEnum.BACKSPACE),
    ("\x08", KeyInputEnum.BACKSPACE),
    (" ", KeyInputEnum.SPACE),
    # --- NAVIGATION & EDITING (ANSI) ---
    ("\x1b[A", KeyInputEnum.UP),
    ("\x1b[B", KeyInputEnum.DOWN),
    ("\x1b[C", KeyInputEnum.RIGHT),
    ("\x1b[D", KeyInputEnum.LEFT),
    ("\x1b[H", KeyInputEnum.HOME),
    ("\x1b[F", KeyInputEnum.END),
    ("\x1b[5~", KeyInputEnum.PAGE_UP),
    ("\x1b[6~", KeyInputEnum.PAGE_DOWN),
    ("\x1b[2~", KeyInputEnum.INSERT),
    ("\x1b[3~", KeyInputEnum.DELETE),
    # --- FUNCTION KEYS (VT100/XTERM) ---
    ("\x1bOP", KeyInputEnum.F1),
    ("\x1bOQ", KeyInputEnum.F2),
    ("\x1bOR", KeyInputEnum.F3),
    ("\x1bOS", KeyInputEnum.F4),
    ("\x1b[15~", KeyInputEnum.F5),
    ("\x1b[17~", KeyInputEnum.F6),
    ("\x1b[18~", KeyInputEnum.F7),
    ("\x1b[19~", KeyInputEnum.F8),
    ("\x1b[20~", KeyInputEnum.F9),
    ("\x1b[21~", KeyInputEnum.F10),
    ("\x1b[23~", KeyInputEnum.F11),
    ("\x1b[24~", KeyInputEnum.F12),
    # --- ALPHANUMERIC (SAMPLES OF RANGES) ---
    ("a", KeyInputEnum.CHAR),
    ("z", KeyInputEnum.CHAR),
    ("A", KeyInputEnum.CHAR),
    ("Z", KeyInputEnum.CHAR),
    ("0", KeyInputEnum.CHAR),
    ("9", KeyInputEnum.CHAR),
    # --- SYMBOLS / SHIFTED KEYS ---
    ("!", KeyInputEnum.CHAR),
    ("@", KeyInputEnum.CHAR),
    ("#", KeyInputEnum.CHAR),
    ("$", KeyInputEnum.CHAR),
    ("%", KeyInputEnum.CHAR),
    ("^", KeyInputEnum.CHAR),
    ("&", KeyInputEnum.CHAR),
    ("*", KeyInputEnum.CHAR),
    ("(", KeyInputEnum.CHAR),
    (")", KeyInputEnum.CHAR),
    ("_", KeyInputEnum.CHAR),
    ("+", KeyInputEnum.CHAR),
    ("{", KeyInputEnum.CHAR),
    ("}", KeyInputEnum.CHAR),
    ("|", KeyInputEnum.CHAR),
    (":", KeyInputEnum.CHAR),
    ('"', KeyInputEnum.CHAR),
    ("<", KeyInputEnum.CHAR),
    (">", KeyInputEnum.CHAR),
    ("?", KeyInputEnum.CHAR),
    ("~", KeyInputEnum.CHAR),
]

# Add remaining printable ASCII characters dynamically to ensure 100% coverage
for i in range(33, 127):
    char = chr(i)
    # Don't duplicate keys already explicitly mapped to special Enums
    if not any(char == pair[0] for pair in FULL_KEYBOARD_SPEC):
        FULL_KEYBOARD_SPEC.append((char, KeyInputEnum.CHAR))

# --- THE TEST SUITE ---


@pytest.mark.parametrize("raw_sequence, expected_identifier", FULL_KEYBOARD_SPEC)
def test_driver_handles_every_standard_key(raw_sequence, expected_identifier):
    """
    Tests the DefaultInputDriver against an exhaustive external list
    of all standard keyboard inputs.
    """
    driver = DefaultInputDriver()
    driver._buffer = [raw_sequence]

    payloads = driver.poll()

    assert len(payloads) == 1, f"Failed to parse key: {repr(raw_sequence)}"

    payload = payloads[0]
    assert (
        payload.identifier == expected_identifier
    ), f"Mismatch for {repr(raw_sequence)}: Expected {expected_identifier}, got {payload.identifier}"

    assert (
        payload.raw_data == raw_sequence
    ), f"Raw data corruption for {repr(raw_sequence)}: Got {repr(payload.raw_data)}"


def test_lexer_handles_combined_stream():
    """
    Final stress test: Verifies the driver can handle a 'slam' of
    multiple keys arriving in a single buffer chunk.
    """
    driver = DefaultInputDriver()
    # Sequence: 'ls' + Enter + Up Arrow + ' ' + F1
    # l, s, \r, \x1b[A, \x20, \x1bOP
    stream = "ls\r\x1b[A \x1bOP"
    driver._buffer = [stream]

    payloads = driver.poll()

    expected_sequence = [
        KeyInputEnum.CHAR,  # l
        KeyInputEnum.CHAR,  # s
        KeyInputEnum.ENTER,  # \r
        KeyInputEnum.UP,  # \x1b[A
        KeyInputEnum.SPACE,  # ' '
        KeyInputEnum.F1,  # \x1bOP
    ]

    assert len(payloads) == len(expected_sequence)
    for i, expected in enumerate(expected_sequence):
        assert payloads[i].identifier == expected
