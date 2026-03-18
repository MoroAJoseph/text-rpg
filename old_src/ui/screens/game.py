from old_src.models.type_models import UIActionsEnum

from ..components.screen import UIScreen


class GameScreen(UIScreen):

    def draw(self, buffer):
        buffer.write(2, 1, "LOCATION: The Dusty Outpost")
        buffer.write(2, 2, "─" * 30)
        buffer.write(5, 5, "@ <--- You are here")

    def handle_action(self, action: UIActionsEnum):
        # Game logic handled elsewhere (GameManager)
        return False


GAME_SCREEN = GameScreen()
