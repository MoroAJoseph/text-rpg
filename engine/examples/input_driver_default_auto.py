import time
from typing import List

from engine.domains.input.drivers.default import DefaultInputDriver
from engine.domains.input.enums import (
    InputStateEnum,
    KeyInputEnum,
    MouseInputEnum,
    ScrollInputEnum,
)


def test_default_driver():
    # Initialize driver with config parameters
    driver = DefaultInputDriver(raw_mode=True, intercept_signals=True)

    print("--- Starting Driver Logic Test ---")

    # 1. Test Static Key Map (Single Characters)
    static_tests = {
        "\r": KeyInputEnum.ENTER,
        "\n": KeyInputEnum.ENTER,
        "\t": KeyInputEnum.TAB,
        "\x1b": KeyInputEnum.ESCAPE,
        "\x7f": KeyInputEnum.BACKSPACE,
        "\x08": KeyInputEnum.BACKSPACE,
        " ": KeyInputEnum.SPACE,
        "a": KeyInputEnum.CHAR,
        "Z": KeyInputEnum.CHAR,
        "1": KeyInputEnum.CHAR,
        "$": KeyInputEnum.CHAR,
    }
    for raw, expected in static_tests.items():
        driver._buffer.append(raw)
        payloads = driver.poll()
        result = payloads[0]
        print(
            f"Static: {repr(raw)} -> {result.identifier.name} | Pass: {result.identifier == expected}"
        )

    # 2. Test ANSI Sequences (Navigation & Function Keys)
    ansi_tests = {
        # Navigation
        "\x1b[A": KeyInputEnum.UP,
        "\x1b[B": KeyInputEnum.DOWN,
        "\x1b[C": KeyInputEnum.RIGHT,
        "\x1b[D": KeyInputEnum.LEFT,
        "\x1b[H": KeyInputEnum.HOME,
        "\x1b[F": KeyInputEnum.END,
        "\x1b[5~": KeyInputEnum.PAGE_UP,
        "\x1b[6~": KeyInputEnum.PAGE_DOWN,
        "\x1b[2~": KeyInputEnum.INSERT,
        "\x1b[3~": KeyInputEnum.DELETE,
        # Function Keys
        "\x1bOP": KeyInputEnum.F1,
        "\x1bOQ": KeyInputEnum.F2,
        "\x1bOR": KeyInputEnum.F3,
        "\x1bOS": KeyInputEnum.F4,
        "\x1b[15~": KeyInputEnum.F5,
        "\x1b[17~": KeyInputEnum.F6,
        "\x1b[18~": KeyInputEnum.F7,
        "\x1b[19~": KeyInputEnum.F8,
        "\x1b[20~": KeyInputEnum.F9,
        "\x1b[21~": KeyInputEnum.F10,
        "\x1b[23~": KeyInputEnum.F11,
        "\x1b[24~": KeyInputEnum.F12,
    }

    for seq, expected in ansi_tests.items():
        driver._buffer.append(seq)
        payloads = driver.poll()
        result = payloads[0]
        print(
            f"ANSI: {repr(seq)} -> {result.identifier.name} | Pass: {result.identifier == expected}"
        )

    # 3. Test SGR Mouse Sequences
    # Format: \x1b[<button;x;y;M(press)/m(release)
    mouse_tests = [
        # Standard Buttons (Press/Release)
        ("\x1b[<0;10;20M", MouseInputEnum.LEFT, InputStateEnum.PRESSED, (10, 20)),
        ("\x1b[<0;10;20m", MouseInputEnum.LEFT, InputStateEnum.RELEASED, (10, 20)),
        ("\x1b[<1;15;25M", MouseInputEnum.MIDDLE, InputStateEnum.PRESSED, (15, 25)),
        ("\x1b[<1;15;25m", MouseInputEnum.MIDDLE, InputStateEnum.RELEASED, (15, 25)),
        ("\x1b[<2;50;100M", MouseInputEnum.RIGHT, InputStateEnum.PRESSED, (50, 100)),
        ("\x1b[<2;50;100m", MouseInputEnum.RIGHT, InputStateEnum.RELEASED, (50, 100)),
        # Scroll
        ("\x1b[<64;5;5M", ScrollInputEnum.UP, InputStateEnum.PRESSED, (5, 5)),
        ("\x1b[<65;5;5M", ScrollInputEnum.DOWN, InputStateEnum.PRESSED, (5, 5)),
        # Unknown Button (Edge Case)
        ("\x1b[<3;0;0M", MouseInputEnum.DEFAULT, InputStateEnum.PRESSED, (0, 0)),
    ]
    for raw, expected_id, expected_state, expected_coords in mouse_tests:
        driver._buffer.append(raw)
        payloads = driver.poll()
        result = payloads[0]

        success = (
            result.identifier == expected_id
            and result.state == expected_state
            and result.coords == expected_coords
        )
        print(
            f"Mouse: {raw} -> {result.identifier.name} ({result.state.name}) at {result.coords} | Pass: {success}"
        )

    # 4. Test Stream Buffering (Mixed Input)
    # Simulating "a", "Up Arrow", and "Left Click" arriving in one buffer string
    mixed_input = "a\x1b[A\x1b[<0;5;5M"
    driver._buffer.append(mixed_input)
    payloads = driver.poll()

    print(f"\nMixed Stream Test (Length: {len(payloads)}):")
    expected_ids = [KeyInputEnum.CHAR, KeyInputEnum.UP, MouseInputEnum.LEFT]
    for i, p in enumerate(payloads):
        print(
            f"  Token {i}: {p.identifier.name} | Pass: {p.identifier == expected_ids[i]}"
        )


if __name__ == "__main__":
    test_default_driver()
