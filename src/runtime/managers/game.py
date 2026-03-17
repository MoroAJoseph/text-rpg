import sys
import time
from logging import Logger
from src.runtime.core.logger import LOGGER
from src.runtime.core.event_bus import EVENT_BUS
from src.models.type_models import (
    ExitCodeEnum,
    ExitRequest,
    GameStateEnum,
    KeyInputEnum,
    KeyInputEvent,
    TelemetryData,
    TelemetryEventsEnum,
    UIScreensEnum,
    UIMenusEnum,
    Event,
    EventTypeEnum,
    GameEventsEnum,
    UIEventsEnum,
)
from .input import INPUT_MANAGER

DEBUG_MODE = True


class GameManager:
    """Singleton: manages game state, actions, and exit handling via events."""

    _instance = None

    TARGET_FPS: int = 60
    FRAME_TIME: float = 1.0 / TARGET_FPS

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, logger: Logger):
        if self._initialized:
            return
        self.logger = logger
        self.show_debug = DEBUG_MODE
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
        if self.show_debug:
            EVENT_BUS.subscribe(KeyInputEnum.ANY, self._handle_debug_input)

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

    def _handle_debug_input(self, event: Event):
        """Intersects raw input for engine-level debug commands."""
        if not isinstance(event.data, KeyInputEvent):
            return

        # Toggle Debug Overlay with backtick
        if event.data.char == "`":
            self.show_debug = not self.show_debug
            self.logger.info(
                f"Debug Overlay: {'ENABLED' if self.show_debug else 'DISABLED'}"
            )

            # Notify UIManager to show/hide the component
            EVENT_BUS.emit(
                Event(
                    type=EventTypeEnum.UI,
                    name=UIEventsEnum.RENDER,  # Forcing render will check the new flag
                )
            )

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
        """Runs the main loop with a frame rate cap."""
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

        while self.state == GameStateEnum.MAIN:
            start_time = time.perf_counter()

            # 1. Process Logic/Events
            EVENT_BUS.process()

            # 2. Handle Exit
            if self.active_exit_request:
                break

            # 3. Calculate Sleep & Telemetry
            end_time = time.perf_counter()
            elapsed = end_time - start_time

            # Calculate how long we need to wait to stay at 60 FPS
            sleep_time = self.FRAME_TIME - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Re-measure for accurate telemetry
            total_frame_time = time.perf_counter() - start_time
            self._emit_telemetry(total_frame_time)

        INPUT_MANAGER.stop()

    # --- Event Emitters ---

    def _emit_telemetry(self, dt: float):
        fps = 1.0 / dt if dt > 0 else 0

        EVENT_BUS.emit(
            Event(
                type=EventTypeEnum.TELEMETRY,
                name=TelemetryEventsEnum.UPDATE,
                data=TelemetryData(fps=fps),
            )
        )

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
