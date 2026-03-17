from src.ui.components.buffer import UIBuffer
from src.ui.components.overlay import UIOverlay
from src.models.type_models import UIActionsEnum


class BackgroundOverlay(UIOverlay):
    """Full-screen dimmed overlay behind menus with configurable intensity."""

    def __init__(self, fg_dim: str = "90", bg_dim: str = "40", char: str = " "):
        super().__init__()
        self.fg_dim = fg_dim
        self.bg_dim = bg_dim
        self.char = char

    def draw(self, buffer: UIBuffer):
        # Apply dim to the entire buffer
        buffer.dim(fg_dim=self.fg_dim, bg_dim=self.bg_dim)

    def handle_action(self, action: UIActionsEnum):
        return False
