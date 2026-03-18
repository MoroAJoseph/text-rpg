from old_src.models.type_models import UIActionsEnum

from .screen import UIScreen


class Notification(UIScreen):
    def draw(self, buffer):
        text = "NOTIFICATION"
        # Top-right corner
        x = buffer.width - len(text) - 5
        y = 1
        self.draw_box(buffer, x, y, len(text) + 4, 3)
        buffer.write(x + 2, y + 1, text)

    def handle_action(self, action: UIActionsEnum) -> bool:
        return False
