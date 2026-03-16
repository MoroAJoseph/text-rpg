from ui.components.screen import UIScreen


class MainGameScreen(UIScreen):
    def draw(self, buffer):
        buffer.write(2, 1, "LOCATION: The Dusty Outpost")
        buffer.write(2, 2, "─" * 30)
        buffer.write(5, 5, "@ <--- You are here")

    def handle_input(self, user_input):
        pass
