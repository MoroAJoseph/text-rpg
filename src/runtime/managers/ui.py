import os, shutil
from logging import Logger
import sys
from typing import List
from runtime.managers.input import InputManager
from ui.buffer import UIBuffer
from ui.components.overlay import UIOverlay
from ui.components.screen import UIScreen


class UIManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger: Logger):
        if self._initialized:
            return
        self.logger: Logger = logger
        self.base_screen: UIScreen
        self.overlays: List[UIOverlay] = []
        self._initialized: bool = True

    def set_screen(self, screen: UIScreen):
        self.base_screen = screen

    def push_overlay(self, overlay: UIOverlay):
        self.overlays.append(overlay)

    def pop_overlay(self):
        if self.overlays:
            self.overlays.pop()

    def render(self):
        # Dimensions
        terminal_width, terminal_height = shutil.get_terminal_size()
        safe_height = max(1, terminal_height - 1)

        # Buffer
        buffer = UIBuffer(terminal_width, safe_height)

        # Draw Layers
        if self.base_screen:
            self.base_screen.draw(buffer)
        for overlay in self.overlays:
            overlay.draw(buffer)

        # Move cursor to top-left
        sys.stdout.write("\033[2J\033[3J\033[H")

        # Render the buffer
        buffer.render_to_terminal()

        # Clear everything from the current cursor position to the bottom of the screen
        # This deletes the 'extra' output that causes the scrollbar
        sys.stdout.write("\033[J")
        sys.stdout.flush()

    def get_input(self) -> str:
        """Gets a single mapped keystroke."""
        raw = InputManager.get_key()
        return InputManager.map_key(raw)

    def get_string(self, prompt: str = "> ") -> str:
        """Fallback to standard input for typing names/strings."""
        try:
            return input(prompt)
        except EOFError:
            return ""

    def process_input(self, user_input: str):
        # Determine the current active layer
        target: UIOverlay | UIScreen = (
            self.overlays[-1] if self.overlays else self.base_screen
        )

        # Only process if we actually have a target and non-empty input
        if target and user_input:
            # Use strip() for menus, but consider if you need raw input for gameplay
            self.logger.debug(
                f"Processing input '{user_input}' for {type(target).__name__}"
            )
            target.handle_input(user_input.strip())
