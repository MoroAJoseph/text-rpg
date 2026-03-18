import time
from typing import List, Dict
from blessed import Terminal
from blessed.keyboard import Keystroke

from engine.core import DomainDriver
from ..dataclasses import InputEvent
from ..enums import InputStateEnum, KeyInputEnum, ScrollInputEnum


class BlessedInputDriver(DomainDriver):
    """
    Blessed-specific implementation of DomainDriver.
    Maps terminal sequences to normalized Engine identifiers.
    """

    # Mapping Blessed's named keys to internal Enums
    KEY_MAP: Dict[str, KeyInputEnum] = {
        "KEY_UP": KeyInputEnum.UP,
        "KEY_DOWN": KeyInputEnum.DOWN,
        "KEY_LEFT": KeyInputEnum.LEFT,
        "KEY_RIGHT": KeyInputEnum.RIGHT,
        "KEY_ENTER": KeyInputEnum.ENTER,
        "KEY_ESCAPE": KeyInputEnum.ESCAPE,
        "KEY_DELETE": KeyInputEnum.DELETE,
        "KEY_BACKSPACE": KeyInputEnum.BACKSPACE,
        "KEY_TAB": KeyInputEnum.TAB,
        "KEY_HOME": KeyInputEnum.HOME,
        "KEY_END": KeyInputEnum.END,
        "KEY_PGUP": KeyInputEnum.PAGE_UP,
        "KEY_PGDOWN": KeyInputEnum.PAGE_DOWN,
        "KEY_INSERT": KeyInputEnum.INSERT,
        " ": KeyInputEnum.SPACE,
        "\n": KeyInputEnum.ENTER,
        "\r": KeyInputEnum.ENTER,
    }

    # Add F-Keys dynamically
    for i in range(1, 13):
        KEY_MAP[f"KEY_F{i}"] = getattr(KeyInputEnum, f"F{i}")

    def __init__(self, terminal: Terminal):
        self.term = terminal

    def poll(self) -> List[InputEvent]:
        events: List[InputEvent] = []
        key: Keystroke = self.term.inkey(timeout=0)
        now: float = time.time()

        if not key:
            return events

        # 1. Handle Mouse/Scroll decoding
        if key.is_sequence and key.name == "KEY_MOUSE":
            # Blessed mouse events are decoded into: [button_code, x, y]
            # Scroll Up is usually button 4 (code 64 or 4)
            # Scroll Down is usually button 5 (code 65 or 5)
            # The 'code' attribute in Blessed for mouse sequences often maps:
            # 64 = Scroll Up, 65 = Scroll Down

            if key.code == 64:
                events.append(
                    InputEvent(
                        identifier=ScrollInputEnum.UP,
                        state=InputStateEnum.PRESSED,
                        timestamp=now,
                        raw_data="scroll",
                    )
                )
            elif key.code == 65:
                events.append(
                    InputEvent(
                        identifier=ScrollInputEnum.DOWN,
                        state=InputStateEnum.PRESSED,
                        timestamp=now,
                        raw_data="scroll",
                    )
                )
            return events

        # 2. Standard Keyboard Logic
        name = key.name if key.name else str(key)

        if name in self.KEY_MAP:
            mapped_id = self.KEY_MAP[name]
        elif len(str(key)) == 1:
            mapped_id = KeyInputEnum.CHAR
        else:
            mapped_id = KeyInputEnum.DEFAULT

        events.append(
            InputEvent(
                identifier=mapped_id,
                state=InputStateEnum.PRESSED,
                timestamp=now,
                raw_data=str(key),
            )
        )
        return events

    def shutdown(self) -> None:
        """Satisfies DomainDriver protocol. Cleanup is handled by Blessed's context."""
        pass
