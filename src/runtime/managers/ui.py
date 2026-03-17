import shutil
import sys
from logging import Logger
from typing import Dict, List, Tuple, Callable

from src.runtime.logger import LOGGER
from src.runtime.event_bus import EVENT_BUS
from src.ui.components.buffer import UIBuffer
from src.ui.components.background_overlay import BackgroundOverlay
from src.ui.components.overlay import UIOverlay
from src.ui.components.screen import UIScreen
from src.ui.menus.main import MAIN_MENU
from src.ui.menus.welcome import WELCOME_MENU
from src.ui.screens.game import GAME_SCREEN
from src.ui.screens.title import TITLE_SCREEN
from src.models.type_models import (
    EventTypeEnum,
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
        self.base_screen: UIScreen | None = None
        self.overlays: List[UIOverlay] = []
        self.screens: Dict[UIScreensEnum, UIScreen] = {}
        self.menus: Dict[UIMenusEnum, UIOverlay] = {}

        # Hitbox Registry: (x1, y1, x2, y2) -> Callback
        self.hitboxes: List[Tuple[int, int, int, int, Callable]] = []

        self._initialized = True
        self.logger.info("UIManager (Rich Input) initialized.")
        self._register_event_listeners()

    def _register_event_listeners(self):
        EVENT_BUS.subscribe(UIEventsEnum.RENDER, self._handle_render)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_SCREEN, self._handle_change_screen)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_MENU, self._handle_change_menu)
        EVENT_BUS.subscribe(UIEventsEnum.CLOSE_MENU, self._handle_close_menu)

        # Subscribe to broad hardware categories
        EVENT_BUS.subscribe(KeyInputEnum.ANY, self._handle_key_input)
        # Subscribe to specific keys that map to UI actions
        for key in [
            KeyInputEnum.UP,
            KeyInputEnum.DOWN,
            KeyInputEnum.ENTER,
            KeyInputEnum.ESCAPE,
        ]:
            EVENT_BUS.subscribe(key, self._handle_key_input)

        # Subscribe to mouse interactions
        EVENT_BUS.subscribe(EventTypeEnum.INPUT, self._handle_generic_input)

    # --- Input Handling ---

    def _map_key_to_action(self, key: KeyInputEnum):
        mapping = {
            KeyInputEnum.UP: UIActionsEnum.NAV_UP,
            KeyInputEnum.DOWN: UIActionsEnum.NAV_DOWN,
            KeyInputEnum.LEFT: UIActionsEnum.NAV_LEFT,
            KeyInputEnum.RIGHT: UIActionsEnum.NAV_RIGHT,
            KeyInputEnum.ENTER: UIActionsEnum.SELECT,
            KeyInputEnum.ESCAPE: UIActionsEnum.BACK,
        }
        return mapping.get(key)

    def _handle_generic_input(self, event: Event):
        """Routes MouseInputEvents and generic input data."""
        if isinstance(event.data, MouseInputEvent):
            self._process_mouse(event.data)

    def _handle_key_input(self, event: Event):
        """Processes KeyInputEvents into UI Actions."""
        # Type guard: Ensure data is not None and is a KeyInputEvent
        if not isinstance(event.data, KeyInputEvent):
            self.logger.debug("Received key event with invalid or missing data.")
            return

        # Now the type checker knows key_event is definitely a KeyInputEvent
        key_event: KeyInputEvent = event.data

        if key_event.state != InputStateEnum.DOWN:
            return

        action = self._map_key_to_action(key_event.key)
        if not action:
            return

        target = self.overlays[-1] if self.overlays else self.base_screen
        if target and target.handle_action(action):
            EVENT_BUS.emit(Event(type=EventTypeEnum.UI, name=UIEventsEnum.RENDER))

    def _process_mouse(self, mouse_event: MouseInputEvent):
        """Checks mouse coordinates against the hitbox registry."""
        # Check for hover or click
        for x1, y1, x2, y2, callback in self.hitboxes:
            if x1 <= mouse_event.x <= x2 and y1 <= mouse_event.y <= y2:
                callback(mouse_event)
                # If a click happened or hover state changed, we likely need a render
                EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    # --- Event Handlers ---

    def _handle_change_screen(self, event: Event):
        """Processes screen change requests from the EventBus."""
        if isinstance(event.data, UIScreensEnum):
            self.show_screen(event.data)
            self.render()

    def _handle_change_menu(self, event: Event):
        """Processes menu push requests from the EventBus."""
        if isinstance(event.data, UIMenusEnum):
            self.show_menu(event.data)
            self.render()

    def _handle_close_menu(self, _: Event):
        """Processes menu pop requests from the EventBus."""
        self.pop_menu()
        self.render()

    # --- Screen/Menu Controls ---

    def register_screen(self, enum: UIScreensEnum, screen: UIScreen):
        self.screens[enum] = screen

    def register_menu(self, enum: UIMenusEnum, menu: UIOverlay):
        self.menus[enum] = menu

    def show_screen(self, enum: UIScreensEnum):
        if screen := self.screens.get(enum):
            self.base_screen = screen
            self.overlays.clear()
            self.hitboxes.clear()  # Clear interaction areas on screen change
        else:
            self.logger.warning(f"Screen {enum} not registered.")

    def show_menu(self, enum: UIMenusEnum):
        if menu := self.menus.get(enum):
            self.overlays.append(BackgroundOverlay())
            self.overlays.append(menu)
        else:
            self.logger.warning(f"Menu {enum} not registered.")

    def pop_menu(self):
        if self.overlays:
            self.overlays.pop()  # Remove menu
            if self.overlays and isinstance(self.overlays[-1], BackgroundOverlay):
                self.overlays.pop()  # Remove dimming

    # --- Rendering ---

    def _handle_render(self, event: Event):
        self.render()

    def render(self):
        # Always clear hitboxes before a redraw so components can re-register them
        self.hitboxes.clear()

        tw, th = shutil.get_terminal_size()
        buffer = UIBuffer(tw, max(1, th - 1))

        if self.base_screen:
            self.base_screen.draw(buffer)
        for overlay in self.overlays:
            overlay.draw(buffer)

        # Move cursor to home and write buffer
        sys.stdout.write("\033[H")
        buffer.render_to_terminal()
        sys.stdout.flush()


UI_MANAGER = UIManager(logger=LOGGER)
UI_MANAGER.register_screen(UIScreensEnum.TITLE, TITLE_SCREEN)
UI_MANAGER.register_screen(UIScreensEnum.GAME, GAME_SCREEN)
UI_MANAGER.register_menu(UIMenusEnum.MAIN, MAIN_MENU)
UI_MANAGER.register_menu(UIMenusEnum.WELCOME, WELCOME_MENU)
