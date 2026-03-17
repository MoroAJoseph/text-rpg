import shutil
import sys
from logging import Logger
from typing import Dict
from src.runtime.logger import LOGGER
from src.runtime.event_bus import EVENT_BUS
from src.ui.buffer import UIBuffer
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
    InputEventsEnum,
)


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
        self.base_screen: UIScreen | None = None
        self.overlays: list[UIOverlay] = []
        self.screens: Dict[UIScreensEnum, UIScreen] = {}
        self.menus: Dict[UIMenusEnum, UIOverlay] = {}
        self._initialized = True
        self.logger.info("UIManager initialized.")
        self._register_event_listeners()

    def _map_input_to_action(self, key: InputEventsEnum):
        mapping = {
            InputEventsEnum.KEY_ARROW_UP: UIActionsEnum.NAV_UP,
            InputEventsEnum.KEY_ARROW_DOWN: UIActionsEnum.NAV_DOWN,
            InputEventsEnum.KEY_ARROW_LEFT: UIActionsEnum.NAV_LEFT,
            InputEventsEnum.KEY_ARROW_RIGHT: UIActionsEnum.NAV_RIGHT,
            InputEventsEnum.KEY_ENTER: UIActionsEnum.SELECT,
            InputEventsEnum.KEY_ESCAPE: UIActionsEnum.BACK,
        }
        return mapping.get(key)

    # --- Event Handlers ---

    def _register_event_listeners(self):
        EVENT_BUS.subscribe(UIEventsEnum.RENDER, self._handle_render)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_SCREEN, self._handle_change_screen)
        EVENT_BUS.subscribe(UIEventsEnum.CHANGE_MENU, self._handle_change_menu)
        EVENT_BUS.subscribe(UIEventsEnum.CLOSE_MENU, self._handle_close_menu)

        for key_event in [
            InputEventsEnum.KEY_ARROW_UP,
            InputEventsEnum.KEY_ARROW_DOWN,
            InputEventsEnum.KEY_ARROW_LEFT,
            InputEventsEnum.KEY_ARROW_RIGHT,
            InputEventsEnum.KEY_ENTER,
            InputEventsEnum.KEY_ESCAPE,
        ]:
            EVENT_BUS.subscribe(key_event, self._handle_input_event)

    def _handle_render(self, event: Event):
        self.render()

    def _handle_change_screen(self, event: Event):
        if isinstance(event.data, UIScreensEnum):
            self.show_screen(event.data)
        else:
            self.logger.warning(f"Invalid screen enum: {event.data}")
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    def _handle_change_menu(self, event: Event):
        if isinstance(event.data, UIMenusEnum):
            self.show_menu(event.data)
        else:
            self.logger.warning(f"Invalid menu enum: {event.data}")
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    def _handle_close_menu(self, event: Event):
        self.pop_menu()
        EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    def _handle_input_event(self, event: Event):
        if event.data != "down":
            return
        action = self._map_input_to_action(event.name)
        if not action:
            return
        target = self.overlays[-1] if self.overlays else self.base_screen
        if target and target.handle_action(action):
            EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.RENDER))

    # --- Registration ---
    def register_screen(self, enum: UIScreensEnum, screen: UIScreen):
        self.screens[enum] = screen

    def register_menu(self, enum: UIMenusEnum, menu: UIOverlay):
        self.menus[enum] = menu

    # --- Controls ---
    def show_screen(self, enum: UIScreensEnum):
        screen = self.screens.get(enum)
        if screen:
            self.base_screen = screen
            self.overlays.clear()
            self.logger.debug(f"Screen set to {enum.name} and overlays cleared.")
        else:
            self.logger.warning(f"Screen {enum} not registered.")

    def show_menu(self, enum: UIMenusEnum, fg_dim: str = "10", bg_dim: str = "90"):
        """Display menu with optional dim intensity behind it."""
        menu = self.menus.get(enum)
        if menu and menu not in self.overlays:
            # Add a dimming background overlay first
            dim_overlay = BackgroundOverlay(fg_dim=fg_dim, bg_dim=bg_dim)
            self.overlays.append(dim_overlay)
            # Then add the actual menu on top
            self.overlays.append(menu)
            self.logger.debug(
                f"Menu {enum.name} displayed with background dim fg={fg_dim}, bg={bg_dim}"
            )

    def pop_menu(self):
        if self.overlays:
            removed = self.overlays.pop()
            self.logger.debug(f"Popped menu/overlay {type(removed).__name__}")
            if self.overlays and isinstance(self.overlays[-1], BackgroundOverlay):
                bg_removed = self.overlays.pop()
                self.logger.debug(
                    f"Popped background overlay {type(bg_removed).__name__}"
                )

    # --- Rendering ---

    def render(self):
        terminal_width, terminal_height = shutil.get_terminal_size()
        buffer = UIBuffer(terminal_width, max(1, terminal_height - 1))

        if self.base_screen:
            self.base_screen.draw(buffer)
        for overlay in self.overlays:
            overlay.draw(buffer)

        # Clear screen and flush
        sys.stdout.write("\033[2J\033[3J\033[H")
        buffer.render_to_terminal()
        sys.stdout.flush()


# --- Initialize singleton and register ---
UI_MANAGER = UIManager(logger=LOGGER)
UI_MANAGER.register_screen(UIScreensEnum.TITLE, TITLE_SCREEN)
UI_MANAGER.register_screen(UIScreensEnum.GAME, GAME_SCREEN)
UI_MANAGER.register_menu(UIMenusEnum.MAIN, MAIN_MENU)
UI_MANAGER.register_menu(UIMenusEnum.WELCOME, WELCOME_MENU)
