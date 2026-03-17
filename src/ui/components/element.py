from abc import ABC, abstractmethod

from src.models.type_models import UIActionsEnum


class UIElement(ABC):
    @abstractmethod
    def draw(self, buffer) -> None: ...

    @abstractmethod
    def handle_action(self, action: UIActionsEnum) -> bool: ...

    def draw_box(self, buffer, x, y, w, h, title=""):
        buffer.write(x, y, "┌" + "─" * (w - 2) + "┐")
        buffer.write(x, y + h - 1, "└" + "─" * (w - 2) + "┘")
        for i in range(1, h - 1):
            buffer.write(x, y + i, "│")
            buffer.write(x + w - 1, y + i, "│")
        if title:
            buffer.write(x + 2, y, f"┤ {title} ├")
