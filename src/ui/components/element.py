from abc import ABC, abstractmethod


class UIElement(ABC):
    @abstractmethod
    def draw(self, buffer) -> None: ...

    @abstractmethod
    def handle_input(self, user_input: str) -> None: ...

    def draw_box(self, buffer, x, y, w, h, title=""):
        buffer.write(x, y, "┌" + "─" * (w - 2) + "┐")
        buffer.write(x, y + h - 1, "└" + "─" * (w - 2) + "┘")
        for i in range(1, h - 1):
            buffer.write(x, y + i, "│")
            buffer.write(x + w - 1, y + i, "│")
        if title:
            buffer.write(x + 2, y, f"┤ {title} ├")
