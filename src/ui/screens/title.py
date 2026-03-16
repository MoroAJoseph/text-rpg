from ui.components.screen import UIScreen


class TitleScreen(UIScreen):
    def draw(self, buffer):
        logo = "LOOT STUFF"
        buffer.write((buffer.width - len(logo)) // 2, 5, logo)

    def handle_input(self, user_input):
        pass
