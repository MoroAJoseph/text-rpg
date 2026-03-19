from typing import List, Dict, Optional
import time
from blessed import Terminal
from blessed.keyboard import Keystroke
from ..enums import InputStateEnum, KeyInputEnum, MouseInputEnum, ScrollInputEnum
from ..models import InputPayload
from .base import InputDriver


class BlessedInputDriver(InputDriver):
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

    def __init__(self, terminal: Optional[Terminal] = None, **kwargs):
        """
        Initialize with optional terminal and catch configuration parameters.
        **kwargs handles: raw_mode, intercept_signals, encoding, etc.
        """
        self.term = terminal or Terminal()
        self.params = kwargs

    def poll(self) -> List[InputPayload]:
        # Blessed inkey(0) can return None, a str, or a Keystroke
        key = self.term.inkey(timeout=0)
        if not key or key == "":
            return []

        # SAFE CHECK: Use getattr or check for 'name' attribute
        name = getattr(key, "name", None)

        if name == "KEY_MOUSE":
            return [self._handle_mouse(key)]

        return [self._handle_keyboard(key)]

    def _handle_keyboard(self, key) -> InputPayload:
        # Determine if it's a special sequence or a raw character
        is_seq = getattr(key, "is_sequence", False)
        name = getattr(key, "name", str(key)) if is_seq else str(key)

        if name in self.KEY_MAP:
            identifier = self.KEY_MAP[name]
        elif len(str(key)) == 1:
            identifier = KeyInputEnum.CHAR
        else:
            identifier = KeyInputEnum.DEFAULT

        return InputPayload(
            identifier=identifier,
            state=InputStateEnum.PRESSED,
            timestamp=time.time(),
            raw_data=str(key),
            coords=(0, 0),
        )

    def _handle_mouse(self, key: Keystroke) -> InputPayload:
        button = getattr(key, "button", -1)
        coords = (getattr(key, "x", 0), getattr(key, "y", 0))

        # Handle Scroll (Blessed codes for scroll are usually in the button/code mix)
        # Note: Some terminals report scroll as 64/65 in button or code
        code = getattr(key, "code", -1)
        if code == 64 or button == 64:
            identifier = ScrollInputEnum.UP
        elif code == 65 or button == 65:
            identifier = ScrollInputEnum.DOWN
        else:
            # Standard Buttons: 0: Left, 1: Middle, 2: Right
            btn_map = {
                0: MouseInputEnum.LEFT,
                1: MouseInputEnum.MIDDLE,
                2: MouseInputEnum.RIGHT,
            }
            identifier = btn_map.get(button, MouseInputEnum.DEFAULT)

        return InputPayload(
            identifier=identifier,
            state=InputStateEnum.PRESSED,
            timestamp=time.time(),
            raw_data="mouse",
            coords=coords,
        )
