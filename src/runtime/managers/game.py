import sys
from logging import Logger
from models.enums import ExitCodeEnum, GameStateEnum
from runtime.managers.ui import UIManager


class ExitRequest:
    def __init__(self, code: ExitCodeEnum, message: str):
        self.code = code
        self.message = message


class GameManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger: Logger, ui_manager: UIManager):
        if self._initialized:
            return
        self.logger = logger
        self.ui_manager = ui_manager
        self.state = GameStateEnum.BOOT
        self.active_exit_request: ExitRequest | None = None
        self._initialized = True
        self.logger.info("GameManager initialized via Injection.")

    def bootloader(self):
        from ui.screens.title import TitleScreen
        from ui.menus.main import MainMenu

        self.ui_manager.set_screen(TitleScreen())
        self.ui_manager.push_overlay(MainMenu())
        self.state = GameStateEnum.MAIN
        self.logger.info("Bootloader complete: Title Screen + Main Menu active.")

    def main_loop(self):
        while self.state == GameStateEnum.MAIN:
            self.ui_manager.render()
            key = self.ui_manager.get_input()
            self.ui_manager.process_input(key)

            # Check for the exit request every loop iteration
            if self.active_exit_request:
                break

    def request_exit(self, code: ExitCodeEnum, msg: str):
        """Sets the exit request and transitions the state."""
        self.active_exit_request = ExitRequest(code, msg)
        self.state = GameStateEnum.EXIT
        self.logger.warning(f"Exit requested: {msg} (Code: {code.name})")

    def handle_exit(self):
        """Final cleanup and OS exit."""
        if not self.active_exit_request:
            self.logger.info("System exiting normally (Success).")
            sys.exit(ExitCodeEnum.SUCCESS.value)

        self.logger.info(
            f"System exiting with code {self.active_exit_request.code.value}"
        )
        sys.exit(self.active_exit_request.code.value)
