from src.models.type_models import UIActionsEnum
from ..components.screen import UIScreen


class TitleScreen(UIScreen):
    def draw(self, buffer):
        logo = "LOOT STUFF"
        buffer.write((buffer.width - len(logo)) // 2, 5, logo)

    def handle_action(self, action: UIActionsEnum):
        # Screens don't manage menus; maybe handle keyboard shortcuts if needed
        return False


TITLE_SCREEN = TitleScreen()
