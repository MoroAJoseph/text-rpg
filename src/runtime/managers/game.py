# runtime/managers/game.py
import os
import sys
from logging import Logger
from src.runtime.logger import LOGGER
from src.runtime.event_bus import EVENT_BUS
from src.models.type_models import (
    ExitCodeEnum,
    ExitRequest,
    GameStateEnum,
    UIScreensEnum,
    UIMenusEnum,
    Event,
    EventTypeEnum,
    GameEventsEnum,
    UIEventsEnum,
)
from .input import INPUT_MANAGER


class GameManager:
    """Singleton: manages game state, actions, and exit handling via events."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger: Logger):
        if self._initialized:
            return
        self.logger = logger
        self.state = GameStateEnum.BOOT
        self.active_exit_request: ExitRequest | None = None

        self._initialized = True
        self.logger.info("GameManager initialized.")

        # Register all game-related event handlers
        self._register_event_listeners()

    # --- Event Handlers ---
    def _register_event_listeners(self):
        EVENT_BUS.subscribe(GameEventsEnum.START_GAME, self._handle_start_game)
        EVENT_BUS.subscribe(GameEventsEnum.LOAD_GAME, self._handle_load_game)
        EVENT_BUS.subscribe(GameEventsEnum.SAVE_GAME, self._handle_save_game)
        EVENT_BUS.subscribe(GameEventsEnum.EXIT_GAME, self._handle_exit_game)

    def _handle_start_game(self, event: Event):
        self.logger.info("Event: START_GAME")
        # Directly perform the start-game logic
        EVENT_BUS.emit(
            Event(EventTypeEnum.UI, UIEventsEnum.CHANGE_SCREEN, UIScreensEnum.GAME)
        )
        EVENT_BUS.emit(
            Event(EventTypeEnum.UI, UIEventsEnum.CHANGE_MENU, UIMenusEnum.WELCOME)
        )

    def _handle_load_game(self, event: Event):
        self.logger.info("Event: LOAD_GAME")
        # Directly perform the load-game logic
        # TODO: add actual load logic here
        EVENT_BUS.emit(
            Event(EventTypeEnum.UI, UIEventsEnum.CHANGE_SCREEN, UIScreensEnum.GAME)
        )

    def _handle_save_game(self, event: Event):
        self.logger.info("Event: SAVE_GAME")
        # TODO: implement save logic

    def _handle_exit_game(self, event: Event):
        self.logger.info("Event: EXIT_GAME")

        # Fallback to empty dict if data is None
        data = event.data or {}

        exit_code = data.get("code", ExitCodeEnum.SUCCESS)
        exit_msg = data.get("msg", "No reason provided")

        self.active_exit_request = ExitRequest(exit_code, exit_msg)
        self.state = GameStateEnum.EXIT

        # Clears the screen
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    # --- Boot / Loop ---
    def bootloader(self):
        """Emit events to initialize the UI."""
        EVENT_BUS.emit(
            Event(EventTypeEnum.UI, UIEventsEnum.CHANGE_SCREEN, UIScreensEnum.TITLE)
        )
        EVENT_BUS.emit(
            Event(EventTypeEnum.UI, UIEventsEnum.CHANGE_MENU, UIMenusEnum.MAIN)
        )
        self.state = GameStateEnum.MAIN
        self.logger.info("Bootloader complete: Title + Main Menu active.")

    def main_loop(self):
        """Runs the main loop entirely via EventBus and InputManager."""
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

        while self.state == GameStateEnum.MAIN:

            # Process all queued events
            EVENT_BUS.process()

            # Exit check
            if self.active_exit_request:
                break

        # Stop input manager thread cleanly
        INPUT_MANAGER.stop()

    # --- Exit Handling ---
    def handle_exit(self):
        if not self.active_exit_request:
            self.logger.info("System exiting normally.")
            sys.exit(ExitCodeEnum.SUCCESS.value)

        self.logger.info(
            f"System exiting with code {self.active_exit_request.code.value}"
        )
        sys.exit(self.active_exit_request.code.value)


GAME_MANAGER = GameManager(logger=LOGGER)
