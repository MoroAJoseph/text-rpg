import re
import time
from typing import List, Any, Dict
from ..models import InputPayload
from ..enums import InputStateEnum, KeyInputEnum, MouseInputEnum, ScrollInputEnum
from .base import InputDriver


class DefaultInputDriver(InputDriver):
    """
    Standard fallback driver for manual ANSI sequence parsing.
    Handles streaming buffers containing mixed raw characters and escape sequences.
    """

    STATIC_KEY_MAP: Dict[str, KeyInputEnum] = {
        "\r": KeyInputEnum.ENTER,
        "\n": KeyInputEnum.ENTER,
        "\t": KeyInputEnum.TAB,
        "\x1b": KeyInputEnum.ESCAPE,
        "\x7f": KeyInputEnum.BACKSPACE,
        "\x08": KeyInputEnum.BACKSPACE,
        " ": KeyInputEnum.SPACE,
    }

    ANSI_MAP: Dict[str, KeyInputEnum] = {
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

    def __init__(self, **parameters):
        self.parameters = parameters
        self._buffer: List[str] = []
        self._sgr_re = re.compile(r"\x1b\[<(\d+);(\d+);(\d+)([Mm])")

        # Cache sorted keys by length (descending) to ensure longest-match priority
        self._sorted_ansi_sequences = sorted(
            self.ANSI_MAP.keys(), key=len, reverse=True
        )

    def poll(self) -> List[InputPayload]:
        """Processes all strings in the buffer and returns normalized payloads."""
        events = []
        while self._buffer:
            raw_string = self._buffer.pop(0)
            events.extend(self._tokenize_and_normalize(raw_string))
        return events

    def _tokenize_and_normalize(self, text: str) -> List[InputPayload]:
        """Lexes a raw string into discrete input events."""
        payloads = []
        i = 0
        text_len = len(text)

        while i < text_len:
            # 1. High Priority: SGR Mouse Sequence
            mouse_match = self._sgr_re.match(text[i:])
            if mouse_match:
                payloads.append(self._handle_mouse_and_scroll(mouse_match.group(0)))
                i += len(mouse_match.group(0))
                continue

            # 2. Medium Priority: ANSI Escape Sequences (Longest Match)
            found_ansi = False
            for seq in self._sorted_ansi_sequences:
                if text.startswith(seq, i):
                    payloads.append(self._handle_keyboard(seq))
                    i += len(seq)
                    found_ansi = True
                    break

            if found_ansi:
                continue

            # 3. Low Priority: Single Characters / Static Map
            char = text[i]
            payloads.append(self._handle_keyboard(char))
            i += 1

        return payloads

    def _handle_keyboard(self, raw: str) -> InputPayload:
        """Maps a single token to a Keyboard payload."""
        identifier = KeyInputEnum.DEFAULT

        if raw in self.STATIC_KEY_MAP:
            identifier = self.STATIC_KEY_MAP[raw]
        elif raw in self.ANSI_MAP:
            identifier = self.ANSI_MAP[raw]
        elif len(raw) == 1 and raw.isprintable():
            identifier = KeyInputEnum.CHAR

        return self._create_payload(identifier, InputStateEnum.PRESSED, raw)

    def _handle_mouse_and_scroll(self, raw: str) -> InputPayload:
        """Parses a confirmed SGR mouse sequence."""
        match = self._sgr_re.match(raw)
        if not match:
            return self._create_payload(
                KeyInputEnum.DEFAULT, InputStateEnum.PRESSED, raw
            )

        btn, x, y, state_char = match.groups()
        btn_int, coords = int(btn), (int(x), int(y))
        state = InputStateEnum.PRESSED if state_char == "M" else InputStateEnum.RELEASED

        # Handle Scroll bits
        if btn_int == 64:
            return self._create_payload(
                ScrollInputEnum.UP, InputStateEnum.PRESSED, raw, coords
            )
        if btn_int == 65:
            return self._create_payload(
                ScrollInputEnum.DOWN, InputStateEnum.PRESSED, raw, coords
            )

        # Standard Buttons
        btn_map = {
            0: MouseInputEnum.LEFT,
            1: MouseInputEnum.MIDDLE,
            2: MouseInputEnum.RIGHT,
        }
        identifier = btn_map.get(btn_int, MouseInputEnum.DEFAULT)

        return self._create_payload(identifier, state, raw, coords)

    def _create_payload(
        self, identifier: Any, state: InputStateEnum, raw: str, coords: tuple = (0, 0)
    ) -> InputPayload:
        """Helper to generate standardized payloads."""
        return InputPayload(
            identifier=identifier,
            state=state,
            timestamp=time.perf_counter(),
            raw_data=raw,
            coords=coords,
        )
