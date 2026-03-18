import time
from typing import List, Dict, Optional
from blessed import Terminal
from blessed.keyboard import Keystroke

from ..dataclasses import InputEvent
from ..enums import InputStateEnum, KeyInputEnum


class BlessedInputDriver:
    """
    Blessed-specific implementation of InputProvider.
    Maps terminal-specific keyboard sequences to normalized Engine identifiers.
    """

    # Mapping Blessed's named keys to internal Enums
    KEY_MAP: Dict[str, KeyInputEnum] = {
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
        """
        Initializes the driver with a shared Blessed Terminal instance.

        Args:
            terminal (Terminal): The active Blessed terminal context.
        """
        self.term = terminal

    def poll(self) -> List[InputEvent]:
        """
        Non-blocking poll of terminal input.

        Returns:
            List[InputEvent]: A list of normalized input events captured
                during this frame.
        """
        events: List[InputEvent] = []

        # timeout=0 ensures we don't hang the engine frame
        # inkey() returns a Keystroke object which is also a string
        key: Keystroke = self.term.inkey(timeout=0)
        now: float = time.time()

        if key:
            # Use the key.name if available (e.g., 'KEY_UP'),
            # otherwise use the raw character (e.g., ' ')
            name: str = key.name if key.name else str(key)
            mapped_identifier: KeyInputEnum = self.KEY_MAP.get(
                name, KeyInputEnum.DEFAULT
            )

            # Terminal drivers are typically stream-based (no native 'Key Up').
            # We emit as PRESSED; the InputManager handles decay to RELEASED.
            events.append(
                InputEvent(
                    identifier=mapped_identifier,
                    state=InputStateEnum.PRESSED,
                    timestamp=now,
                    raw_data=name,
                )
            )

        return events
