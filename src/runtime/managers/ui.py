import shutil
import sys
from logging import Logger
from typing import Dict, List, Tuple, Callable

from src.runtime.logger import LOGGER
from src.runtime.event_bus import EVENT_BUS
from src.ui.components.buffer import UIBuffer
from src.ui.components.background_overlay import BackgroundOverlay
from src.ui.components.debug_overlay import DebugOverlay
from src.ui.components.overlay import UIOverlay
from src.ui.components.screen import UIScreen
from src.ui.menus.main import MAIN_MENU
from src.ui.menus.welcome import WELCOME_MENU
from src.ui.screens.game import GAME_SCREEN
from src.ui.screens.title import TITLE_SCREEN
from src.models.type_models import (
    EventTypeEnum,
    TelemetryData,
    TelemetryEventsEnum,
    UIActionsEnum,
    UIScreensEnum,
    UIMenusEnum,
    Event,
    UIEventsEnum,
    KeyInputEnum,
    InputStateEnum,
    KeyInputEvent,
    MouseInputEvent,
)


class UIManager:
    """Manages UI state, focus, rendering, and input routing via hitboxes."""

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

        # Flag managed by GameManager debug toggle
        self.show_debug = True
        self.debug_overlay = DebugOverlay()

        self.base_screen: UIScreen | None = None
        self.overlays: List[UIOverlay] = []
        self.screens: Dict[UIScreensEnum, UIScreen] = {}
        self.menus: Dict[UIMenusEnum, UIOverlay] = {}

        # Hitbox Registry: (x1, y1, x2, y2) -> Callback
        self.hitboxes: List[Tuple[int, int, int, int, Callable]] = []

        self._initialized = True
        self.logger.info("UIManager initialized (Telemetry delegated).")
        self._register_event_listeners()

    def _register_event_listeners(self):
        # Core UI Events
        EVENT_BUS.subscribe(UIEventsEnum.RENDER, self._handle_render)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_SCREEN, self._handle_change_screen)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_MENU, self._handle_change_menu)
        EVENT_BUS.subscribe(UIEventsEnum.CLOSE_MENU, self._handle_close_menu)

        # Input Subscriptions
        EVENT_BUS.subscribe(KeyInputEnum.ANY, self._handle_key_input)
        EVENT_BUS.subscribe(EventTypeEnum.INPUT, self._handle_generic_input)

    # --- Input Processing ---

    def _handle_generic_input(self, event: Event):
        if isinstance(event.data, MouseInputEvent):
            self._process_mouse(event.data)

    def _handle_key_input(self, event: Event):
        if (
            not isinstance(event.data, KeyInputEvent)
            or event.data.state != InputStateEnum.DOWN
        ):
            return

        key_map = {
            KeyInputEnum.UP: UIActionsEnum.NAV_UP,
            KeyInputEnum.DOWN: UIActionsEnum.NAV_DOWN,
            KeyInputEnum.LEFT: UIActionsEnum.NAV_LEFT,
            KeyInputEnum.RIGHT: UIActionsEnum.NAV_RIGHT,
            KeyInputEnum.ENTER: UIActionsEnum.SELECT,
            KeyInputEnum.ESCAPE: UIActionsEnum.BACK,
        }

        if action := key_map.get(event.data.key):
            target = self.overlays[-1] if self.overlays else self.base_screen
            if target and target.handle_action(action):
                self.render()

    def _process_mouse(self, mouse_event: MouseInputEvent):
        """Standard collision detection for registered hitboxes."""
        for x1, y1, x2, y2, callback in self.hitboxes:
            if x1 <= mouse_event.x <= x2 and y1 <= mouse_event.y <= y2:
                callback(mouse_event)
                # Note: The callback itself should decide if a re-render is needed,
                # but we usually re-render on any interaction to update visual states.
                self.render()

    # --- Registry & State ---

    def register_screen(self, enum: UIScreensEnum, screen: UIScreen):
        self.screens[enum] = screen

    def register_menu(self, enum: UIMenusEnum, menu: UIOverlay):
        self.menus[enum] = menu

    def register_hitbox(self, x1: int, y1: int, x2: int, y2: int, callback: Callable):
        self.hitboxes.append((x1, y1, x2, y2, callback))

    # --- Rendering Heartbeat ---

    def render(self):
        # Reset hitboxes at start of frame
        self.hitboxes.clear()

        tw, th = shutil.get_terminal_size()
        buffer = UIBuffer(tw, max(1, th - 1))

        # Layered Drawing
        if self.base_screen:
            self.base_screen.draw(buffer)
        for overlay in self.overlays:
            overlay.draw(buffer)

        # Telemetry Sync: Send hitbox count to TelemetryManager
        EVENT_BUS.emit(
            Event(
                type=EventTypeEnum.TELEMETRY,
                name=TelemetryEventsEnum.UPDATE,
                data=TelemetryData(active_hitboxes=len(self.hitboxes)),
            )
        )

        if self.show_debug:
            self.debug_overlay.draw(buffer)

        # Final terminal output
        sys.stdout.write("\033[H")
        buffer.render_to_terminal()
        sys.stdout.flush()

    # --- Event Handlers ---

    def _handle_render(self, _: Event):
        self.render()

    def _handle_change_screen(self, event: Event):
        if isinstance(event.data, UIScreensEnum):
            if screen := self.screens.get(event.data):
                self.base_screen = screen
                self.overlays.clear()
                self.render()

    def _handle_change_menu(self, event: Event):
        if isinstance(event.data, UIMenusEnum):
            if menu := self.menus.get(event.data):
                self.overlays.append(BackgroundOverlay())
                self.overlays.append(menu)
                self.render()

    def _handle_close_menu(self, _: Event):
        if self.overlays:
            self.overlays.pop()  # Menu
            if self.overlays and isinstance(self.overlays[-1], BackgroundOverlay):
                self.overlays.pop()  # Dimmer
            self.render()


# Initialize Singleton
UI_MANAGER = UIManager(logger=LOGGER)

# Boot-time Registrations
UI_MANAGER.register_screen(UIScreensEnum.TITLE, TITLE_SCREEN)
UI_MANAGER.register_screen(UIScreensEnum.GAME, GAME_SCREEN)
UI_MANAGER.register_menu(UIMenusEnum.MAIN, MAIN_MENU)
UI_MANAGER.register_menu(UIMenusEnum.WELCOME, WELCOME_MENU)
