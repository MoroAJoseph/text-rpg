import time
from typing import List
from blessed import Terminal
from ..common.enums import KeyInputEnum, InputStateEnum
from ..common.dataclasses import InputEvent


class BlessedInputDriver:
    """The Blessed implementation of an InputProvider."""

    # Mapping Blessed's unique key names to your Engine's KeyInputEnum
    KEY_MAP = {
        "KEY_UP": KeyInputEnum.UP,
        "KEY_DOWN": KeyInputEnum.DOWN,
        "KEY_LEFT": KeyInputEnum.LEFT,
        "KEY_RIGHT": KeyInputEnum.RIGHT,
        "KEY_ENTER": KeyInputEnum.ENTER,
        "KEY_ESCAPE": KeyInputEnum.ESCAPE,
        " ": KeyInputEnum.SPACE,
        "\n": KeyInputEnum.ENTER,
        "\r": KeyInputEnum.ENTER,
        "KEY_BACKSPACE": KeyInputEnum.BACKSPACE,
    }

    def __init__(self, terminal: Terminal):
        self.term = terminal
        # Ensure we are in the correct terminal modes for capturing
        # Note: These usually happen in the main loop context, but driver needs them
        self.last_poll_time = time.perf_counter()

    def poll(self) -> List[InputEvent]:
        """Captures a single keypress from the terminal and returns a list of events."""
        events = []

        # Non-blocking check for input
        # timeout=0 means "check and return immediately"
        key = self.term.inkey(timeout=0)
        now = time.perf_counter()

        if key:
            name = key.name or str(key)
            mapped_key = self.KEY_MAP.get(name, KeyInputEnum.DEFAULT)

            # Since terminal input is 'stream-based', it usually only reports 'PRESSED'.
            # We treat a successful inkey() as a PRESSED state.
            events.append(
                InputEvent(
                    key=mapped_key,
                    state=InputStateEnum.PRESSED,
                    timestamp=now,
                    raw_data=name,
                )
            )

        return events
