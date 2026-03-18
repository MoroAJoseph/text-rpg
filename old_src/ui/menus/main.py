from old_src.runtime.core.event_bus import EVENT_BUS
from old_src.models.type_models import (
    Event,
    EventTypeEnum,
    ExitCodeEnum,
    GameEventsEnum,
    UIActionsEnum,
    UIEventsEnum,
)
from ..components.overlay import UIOverlay


class MainMenu(UIOverlay):
    """Main menu overlay. Handles input events directly as enums."""

    def __init__(self):
        super().__init__()
        self.options = ["New Game", "Load Game", "Exit"]
        self.index = 0

    def draw(self, buffer):
        w, h = 30, 8
        x, y = (buffer.width - w) // 2, (buffer.height - h) // 2
        self.draw_box(buffer, x, y, w, h, "Main Menu")
        for i, opt in enumerate(self.options):
            prefix = " > " if i == self.index else "   "
            buffer.write(x + 4, y + 3 + i, f"{prefix}{opt}")

    def handle_action(self, action: UIActionsEnum) -> bool:
        old_index = self.index

        if action == UIActionsEnum.NAV_UP:
            self.index = (self.index - 1) % len(self.options)

        elif action == UIActionsEnum.NAV_DOWN:
            self.index = (self.index + 1) % len(self.options)

        elif action == UIActionsEnum.SELECT:
            self._execute_selection()
            return False

        return self.index != old_index

    def _execute_selection(self):
        choice = self.options[self.index]
        if choice == "New Game":
            EVENT_BUS.emit(Event(EventTypeEnum.GAME, GameEventsEnum.START_GAME))
        elif choice == "Load Game":
            EVENT_BUS.emit(Event(EventTypeEnum.GAME, GameEventsEnum.LOAD_GAME))
        elif choice == "Exit":
            EVENT_BUS.emit(
                Event(
                    EventTypeEnum.GAME,
                    GameEventsEnum.EXIT_GAME,
                    {"code": ExitCodeEnum.SUCCESS, "msg": "Main Menu Exit"},
                )
            )


MAIN_MENU = MainMenu()
