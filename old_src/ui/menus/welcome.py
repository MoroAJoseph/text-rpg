from old_src.models.type_models import Event, EventTypeEnum, UIActionsEnum, UIEventsEnum
from old_src.runtime.core.event_bus import EVENT_BUS
from ..components.overlay import UIOverlay


class WelcomeMenu(UIOverlay):
    """Simple welcome overlay. Closes on any input."""

    def draw(self, buffer):
        w, h = 40, 5
        x, y = (buffer.width - w) // 2, (buffer.height - h) // 2
        self.draw_box(buffer, x, y, w, h, "WELCOME")
        buffer.write(x + 4, y + 2, "Welcome to the Sandbox, Hero!")

    def handle_action(self, action: UIActionsEnum):
        if action in (UIActionsEnum.SELECT, UIActionsEnum.BACK):
            EVENT_BUS.emit(Event(EventTypeEnum.UI, UIEventsEnum.CLOSE_MENU))
        return True


WELCOME_MENU = WelcomeMenu()
